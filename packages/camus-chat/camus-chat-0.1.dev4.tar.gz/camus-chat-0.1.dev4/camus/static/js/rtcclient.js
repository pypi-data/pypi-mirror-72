'use strict';

import adapter from 'webrtc-adapter';  // eslint-disable-line no-unused-vars

class EventEmitter {
    constructor() {
        this.events = new Map();
    }

    on(event, callback) {
        if (!this.events.has(event)) {
            this.events.set(event, []);
        }

        this.events.get(event).push(callback);
    }

    emit(event, ...args) {
        if (this.events.has(event)) {
            const callbacks = this.events.get(event);
            callbacks.forEach((callback) => {
                callback(...args);
            });
        }
    }
}


class VideoPeer extends EventEmitter {
    constructor(client, groundControl, polite, iceServers=[]) {
        super();
        this.client_id = client.id;
        this.username = client.username;
        this.groundControl = groundControl;
        this.polite = polite;
        this.connection = null;
        this.makingOffer = false;

        this.createPeerConnection(iceServers);
    }

    createPeerConnection(iceServers) {
        const config = {
            sdpSemantics: 'unified-plan',
            iceServers: iceServers,
        };
        this.connection = new RTCPeerConnection(config);

        // Handle incoming tracks from the peer
        this.connection.ontrack = ({track, streams}) => {
            console.log(`[${this.client_id}] ${track.kind} track ${track.id} received`);
            this.emit('track', track, streams);
        };

        this.connection.onconnectionstatechange = (evt) => {
            console.log(`[${this.client_id}] Connection state: ${this.connection.connectionState}`);
            this.emit('connectionstatechange', this.connection.connectionState);
        };

        // Handle failed ICE connections
        this.connection.oniceconnectionstatechange = () => {
            console.log(`[${this.client_id}] Ice connection state: ${this.connection.iceConnectionState}`);
            if (this.connection.iceConnectionState === "failed") {
                this.connection.restartIce();
            }

            this.emit('iceconnectionstatechange', this.connection.iceConnectionState);
        };

        this.connection.onsignalingstatechange = () => {
            console.log(`[${this.client_id}] Signaling state: ${this.connection.signalingState}`);
        };

        this.connection.onicegatheringstatechange = () => {
            console.log(`[${this.client_id}] Ice gathering state: ${this.connection.iceGatheringState}`);
        };

        // Handle (re)negotiation of the connection
        this.connection.onnegotiationneeded = async () => {
            console.log(`[${this.client_id}] onnegotiationneeded`);

            try {
                this.makingOffer = true;
                const offer = await this.connection.createOffer();
                if (this.connection.signalingState !== 'stable') return;
                await this.connection.setLocalDescription(offer);
                const description = this.connection.localDescription.toJSON();
                this.groundControl.sendMessage({
                    receiver: this.client_id,
                    type: description.type,
                    data: description
                });
            } catch(err) {
                console.error(err);
            } finally {
                this.makingOffer = false;
            }
        };

        // Send ICE candidates as they are gathered
        this.connection.onicecandidate = ({candidate}) => {
            if (candidate) {
                //console.log('Gathered ICE candidate: ', candidate);
                this.groundControl.sendMessage({
                    receiver: this.client_id,
                    type: 'icecandidate',
                    data: candidate.toJSON()
                });
            }
        };
    }

    connect() {
        // Adding transceivers triggers onnegotiationneeded()
        this.connection.addTransceiver('video');
        this.connection.addTransceiver('audio');
    }

    get connectionState() {
        return this.connection.connectionState;
    }

    get iceConnectionState() {
        return this.connection.iceConnectionState;
    }

    get iceGatheringState() {
        return this.connection.iceGatheringState;
    }

    get signalingState() {
        return this.connection.signalingState;
    }

    remoteDescription() {
        let description = this.connection.remoteDescription;
        if (description) {
            return description.sdp;
        } else {
            return null;
        }
    }

    async onOffer(offer) {
        /* Perfect negotiation:
         * 1. If we are ready to accept the offer (i.e. we're not in the process of making our
         *    own offer), then set the remote description with the offer.
         * 2. Otherwise, there is an "offer collision". If we are the impolite peer, ignore the
         *    offer. If we are polite, roll back the local description and set the remote
         *    description with the offer.
         * 3. If we aren't ignoring the offer, respond to the peer with an answer.
         */

        console.log(`[${this.client_id}] Processing offer`);
        if (offer.type !== 'offer') {
            throw new Error('type mismatch');
        }

        try {
            const offerCollision = this.makingOffer || this.connection.signalingState !== 'stable';
            console.log(`[${this.client_id}] ? Polite: ${this.polite}`);

            if (offerCollision) {
                if (!this.polite) {
                    console.log(`[${this.client_id}] Reject offer`);
                    return;
                }

                // Polite peer rolls back local description and accepts remote offer
                await Promise.all([
                    this.connection.setLocalDescription({type: "rollback"}),
                    this.connection.setRemoteDescription(offer)
                ]);

            } else {
                // No collision, so accept the remote offer
                await this.connection.setRemoteDescription(offer);
            }

            // Create an answer to the remote offer and send it
            const answer = await this.connection.createAnswer();
            await this.connection.setLocalDescription(answer);

            const description = this.connection.localDescription.toJSON();
            console.log(`[${this.client_id}] Respond to offer`);
            this.groundControl.sendMessage({
                receiver: this.client_id,
                type: description.type,
                data: description
            });
        } catch(err) {
            console.error(err);
        }
    }

    async onAnswer(answer) {
        console.log(`[${this.client_id}] Processing answer`);

        try {
            await this.connection.setRemoteDescription(answer);
        } catch(err) {
            console.error(err);
        }
    }

    async onIceCandidate(candidate) {
        try {
            await this.connection.addIceCandidate(candidate);
        } catch(err) {
            console.error(err);
        }
    }

    async setTrack(track, stream=null) {
        const trackSender = this.connection.getSenders().find(sender =>
            sender.track && sender.track.kind === track.kind);

        if (trackSender) {
            console.log('Replacing track on sender ', trackSender);
            trackSender.track.stop();
            await trackSender.replaceTrack(track);
        } else {
            if (stream) this.connection.addTrack(track, stream);
            else this.connection.addTrack(track);
        }
    }

    getTrack(kind) {
        const trackSender = this.connection.getSenders().find(sender =>
            sender.track && sender.track.kind === kind);

        if (trackSender) return trackSender.track;
        else return null;
    }

    restartIce() {
        this.connection.restartIce();
    }

    shutdown() {
        // Clean up RTCPeerConnection
        if (this.connection !== null) {
            this.connection.getSenders().forEach(sender => {
                if(sender.track) sender.track.stop();
            });

            this.connection.getReceivers().forEach(receiver => {
                if(receiver.track) receiver.track.stop();
            });

            this.connection.close();
            this.connection = null;
        }

        // Say bye to peer
        const time = new Date().getTime();
        const data = {"receiver": this.client_id,
                      "type": "bye",
                      "data": time};
        this.groundControl.sendMessage(data);

        this.emit('shutdown');

        console.log('Shutdown connection with peer ' + this.client_id);
    }
}

class GroundControl {
    constructor() {
        this.connection = null;
        this.datachannel = null;
        this.createConnection();
    }

    createConnection() {
        let config = {
            sdpSemantics: 'unified-plan'
        };
        config.iceServers = [{urls: ['stun:stun.l.google.com:19302']}];
        this.connection = new RTCPeerConnection(config);

        this.connection.addEventListener('iceconnectionstatechange', () => {
            console.log("Ice connection state:", this.connection.iceConnectionState);
            if (this.connection.iceConnectionState === "failed") {
                this.connection.restartIce();
            }
        });

        this.datachannel = this.connection.createDataChannel('data');
        this.datachannel.onopen = (evt) => {
            this.greeting();
        };

        console.log('Connection for Ground Control created');
    }

    connectionState() {
        return this.connection.iceConnectionState;
    }

    async offer() {
        console.log('In groundControl.offer()');
        // Create offer for Ground Control
        const offer = await this.connection.createOffer();
        console.log('created offer', offer);
        await this.connection.setLocalDescription(offer);
        console.log('set local description', this.connection.localDescription);

        // Wait for ice gathering to complete
        while (this.connection.iceGatheringState != 'complete') {
            await new Promise(r => {setTimeout(r, 100)});
        }

        console.log('ice gathering complete');

        // Send the offer and wait for the answer
        console.log('Posting offer to ' + document.URL + '/offer');
        const response = await fetch(document.URL + '/offer', {
            body: JSON.stringify({sdp: this.connection.localDescription.sdp,
                                  type: this.connection.localDescription.type}),
            headers: {'Content-Type': 'application/json'},
            method: 'POST'
        });
        const answer = await response.json();
        await this.connection.setRemoteDescription(answer);
    }

    sendMessage(data) {
        this.datachannel.send(JSON.stringify(data));
        if (data.type === 'offer' || data.type === 'answer' || data.type === 'icecandidate') {
            console.log(`>> Sent ${data.type}: `, data);
        }
    }

    async sendReceiveMessage(data, responseParams) {
        // return a Promise that resolves when an appropriate response is received
        return new Promise((resolve, reject) => {
            // TODO: use message handler?
            function matchResponse(message) {
                for (const key in responseParams) {
                    if (!(message.hasOwnProperty(key) && message[key] === responseParams[key])) {
                        return false;
                    }
                }
                return true;
            }

            let dc = this.datachannel;  // needed to access the datachannel inside the closure
            function onMessage(evt) {
                let message = JSON.parse(evt.data);
                if (matchResponse(message)) {
                    console.log(`Response matched: `, responseParams);
                    dc.removeEventListener('message', onMessage);
                    resolve(message);
                }
            }

            this.datachannel.addEventListener('message', onMessage);
            this.sendMessage(data);
        });
    }

    greeting() {
        const data = {"receiver": "ground control",
                      "type": "greeting",
                      "data": "This is Major Tom to Ground Control: I'm stepping through the door. And the stars look very different today."};
        this.sendMessage(data);
    }

    shutdown() {
        // Stop media tracks
        this.connection.getReceivers().forEach(receiver => {
            receiver.track.stop();
        });

        // Say bye to Ground Control
        const time = new Date().getTime();
        const data = {"receiver": "ground control",
                    "type": "bye",
                    "data": time};
        this.sendMessage(data);

        // Shutdown connections
        this.connection.close();
        this.connection = null;
        this.datachannel = null;

        console.log('Shutdown connection with Ground Control ');
    }
}

class MessageHandler {
    constructor(manager, signaler) {
        this.manager = manager;
        this.signaler = signaler;
        this.messageListeners = [];
        this.handlers = {'ping': this.ping,
                         'pong': this.pong,
                         'text': this.text,
                         'get-room-info': this.getRoomInfo,
                         'room-info': this.roomInfo,
                         'get-ice-servers': this.getIceServers,
                         'ice-servers': this.iceServers,
                         'profile': this.profile,
                         'offer': this.offer,
                         'answer': this.answer,
                         'icecandidate': this.iceCandidate,
                         'greeting': this.greeting,
                         'bye': this.bye
        };
    }

    addMessageListener(messageParams, listener) {
        this.messageListeners.push([messageParams, listener]);
    }

    async handleMessage(message) {
        await this.handlers[message.type].call(this, message);

        this.messageListeners.forEach(([messageParams, listener]) => {
            if (this.match(message, messageParams)) {
                console.log('Calling listener for message: ', message);
                listener(message);
            }

        });
    }

    async ping(message) {
        console.log('<< Received ping: ', message);

        let response = this.emptyMessage();
        response.receiver = message.sender;
        response.type = 'pong';
        response.data = message.data;
        this.signaler.sendMessage(response);
    }

    async pong(message) {
        console.log('<< Received pong: ', message);
    }

    async text(message) {
        console.log('<< Received text: ', message);
        this.manager.textMessages.push(message.data);
    }

    async getRoomInfo(message) {
        console.log('<< Received get-room-info: ', message);
    }

    async roomInfo(message) {
        console.log('<< Received room-info: ', message);
        await this.manager.updatePeers(message.data);
    }

    async getIceServers(message) {
        console.log('<< Received get-ice-servers: ', message);
    }

    async iceServers(message) {
        console.log('<< Received ice-servers: ', message);
    }

    async profile(message) {
        console.log('<< Received profile: ', message);
    }

    async offer(message) {
        console.log('<< Received offer: ', message);

        const peer = await this.manager.getOrCreateVideoPeer({id: message.sender, username: 'Major Tom'});
        if (message.type !== message.data.type){
            throw new Error('! Type mismatch in offer');
        }
        await peer.onOffer(message.data);
    }

    async answer(message) {
        console.log('<< Received answer: ', message);

        const peer = await this.manager.getOrCreateVideoPeer({id: message.sender, username: 'Major Tom'});
        if (message.type !== message.data.type){
            throw new Error('! Type mismatch in answer');
        }
        await peer.onAnswer(message.data);
    }

    async iceCandidate(message) {
        console.log('<< Received icecandidate: ', message);

        const peer = await this.manager.getOrCreateVideoPeer({id: message.sender, username: 'Major Tom'});
        const iceCandidate = new RTCIceCandidate(message.data);
        await peer.onIceCandidate(iceCandidate);
    }

    async greeting(message) {
        console.log('<< Received greeting: ', message);
    }

    async bye(message) {
        console.log('<< Received bye: ', message);

        let client_id = message.sender;
        if (this.manager.videoPeers.has(client_id)) {
            this.manager.videoPeers.get(client_id).shutdown();
            this.manager.videoPeers.delete(client_id);
        }
    }

    emptyMessage() {
        return {sender: '',
                receiver: '',
                type: '',
                data: ''};
    }

    match(message, params) {
        for (const key in params) {
            if (!(message.hasOwnProperty(key) && message[key] === params[key])) {
                return false;
            }
        }
        return true;
    }
}

class Manager extends EventEmitter {
    constructor() {
        super();
        this.username = 'Major Tom';
        this.groundControl = new GroundControl();
        this.videoPeers = new Map();
        this.localVideoStream = null;
        this.videoTrack = null;
        this.audioTrack = null;
        this.textMessages = [];
        this.messageHandler = new MessageHandler(this, this.groundControl);
        this.outbox = [];
        this.id = null;
        this.iceServers = [];
    }

    async setUsername(username) {
        this.username = username;

        const data = {receiver: 'ground control',
                      type: 'profile',
                      data: {username: this.username}
        };
        this.groundControl.sendMessage(data);
        console.log('Set username in manager: ', this.username);
    }

    async setAudioTrack(track) {
        await this.setTrack(track);
        this.audioTrack = track;
    }

    async setVideoTrack(track) {
        await this.setTrack(track);
        this.videoTrack = track;
    }

    async setTrack(track) {
        this.videoPeers.forEach(async (peer, peer_id) => {
            console.log('Replace ' + track.kind + ' track for peer ' + peer_id);
            await peer.setTrack(track, this.localVideoStream);
        });
    }

    toggleAudio() {
        if (this.audioTrack) {
            this.audioTrack.enabled = !this.audioTrack.enabled;
            console.log(this.audioTrack.kind + ' enabled: ' + this.audioTrack.enabled);
        }
    }

    audioEnabled() {
        return this.audioTrack && this.audioTrack.enabled;
    }

    async establishGroundControl() {
        await this.groundControl.offer();
        return this.groundControl;
    }

    async createVideoPeer(client) {
        const peer = new VideoPeer(client, this.groundControl, this.id < client.id, this.iceServers);
        this.videoPeers.set(client.id, peer);
        peer.connect();

        if (this.localVideoStream && this.videoTrack) {
            await peer.setTrack(this.videoTrack, this.localVideoStream);
        }

        if (this.localVideoStream && this.audioTrack) {
            await peer.setTrack(this.audioTrack, this.localVideoStream);
        }

        console.log('Created video peer ', peer.client_id);
        this.emit('videopeer', peer);

        return peer;
    }

    async getOrCreateVideoPeer(client) {
        if (!this.videoPeers.has(client.id)) {
            return await this.createVideoPeer(client);
        }

        return this.videoPeers.get(client.id);
    }

    async findPeers() {
        let roomInfo = await this.get_room_info();
        await this.updatePeers(roomInfo);
    }

    async updatePeers(roomInfo) {
        // Remove peers not in room
        let roomClientIds = roomInfo.clients.map(({id, username}) => id);
        let peerClientIds = Array.from(this.videoPeers.keys());
        let removeIds = peerClientIds.filter(id => !roomClientIds.includes(id));

        removeIds.forEach(async (clientId) => {
            let peer = this.videoPeers.get(clientId);
            peer.shutdown();
            this.videoPeers.delete(clientId);
            console.log('Removed client ', clientId);
        });

        // Add peers in room
        roomInfo.clients.forEach(async (client) => {
            if (client.id !== this.id) {
                await this.getOrCreateVideoPeer(client);
            }
        });

        // Update information for each peer
        this.videoPeers.forEach((peer, peer_id) => {
            let oldUsername = peer.username;
            let client = roomInfo.clients.find(client => client.id === peer_id);
            if (client) {
                peer.username = client.username;
                console.log('Set peer username from ' + oldUsername + ' to ' + peer.username);
            }
        });
    }

    addMessageListener(messageParams, listener) {
        this.messageHandler.addMessageListener(messageParams, listener);
    }

    shutdownVideoPeers() {
        this.videoPeers.forEach((peer, peer_id) => {
            peer.shutdown();
        });

        this.videoPeers.clear();
    }

    async get_self_id() {
        const time = new Date().getTime();
        let data = {"receiver": "ground control",
                    "type": "ping",
                    "data": time};
        let responseParams = {"sender": "ground control",
                            "type": "pong",
                            "data": time};
        let response = await this.groundControl.sendReceiveMessage(data, responseParams);
        return response.receiver;

    }

    async get_room_info() {
        let data = {"receiver": "ground control",
                    "type": "get-room-info"};
        let responseParams = {"sender": "ground control",
                              "type": "room-info"};
        let response = await this.groundControl.sendReceiveMessage(data, responseParams);
        return response.data;
    }

    async getIceServers() {
        const data = {
            'receiver': 'ground control',
            'type': 'get-ice-servers'
        }
        const responseParams = {
            'sender': 'ground control',
            'type': 'ice-servers'
        }
        const response = await this.groundControl.sendReceiveMessage(data, responseParams);
        return response.data;
    }

    async shutdown() {
        this.shutdownVideoPeers();
        await this.groundControl.shutdown();
    }

    async start() {
        await this.establishGroundControl();

        // Set up message handler
        this.groundControl.datachannel.addEventListener('message', (evt) => {
            this.messageHandler.handleMessage(JSON.parse(evt.data));
        });

        // Wait for data channel to open
        while (this.groundControl.datachannel.readyState != 'open') {
            await new Promise(r => {setTimeout(r, 100)});
        }

        this.id = await this.get_self_id();
        this.iceServers = await this.getIceServers();
        await this.findPeers();
    }
}

export {Manager, GroundControl, VideoPeer};
