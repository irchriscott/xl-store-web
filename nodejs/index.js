const http = require('http').createServer().listen(4000);
const io = require('socket.io')(http);
const mysql = require('mysql');


const db = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    port:3306,
    database: "xlstoredb",
});

db.connect((error, data) => {
    if(error) throw error
    console.log("MySQL Connected on port 4000");
});

var baseUrl = "http://127.0.0.1:8000/";
var onlineUsers = [];

io.on("connection", function(socket){
    
    socket.on("userOnline", function(onlineUserData){
        onlineUsers.append(onlineUserData);
        io.emit("getUserOnline", onlineUserData);
    });
    
    //MESSAGES SOCKETS
    
    socket.on("textMessage", function(msgObject){
        io.emit("getTextMessage", msgObject);
    });
    
    socket.on("textTyping", function(data){
        io.emit("getTextTyping", data);
    });
    
    //MESSAGE CALL SOCKETS
    
    socket.on("calling", function(data){
        io.emit("getCall", data);
    });
    
    socket.on("hangup", function(data){
        io.emit("hangupCall", data);
    });
    
    socket.on("pickup", function(data){
        io.emit("pickupCall", data);
    });
    
    socket.on("streaming", function(data){
        io.emit("startStreaming", data);
    });
    
    //MARKET SOCKETS
    
    socket.on("askAccess", function(data){
        io.emit("askAccessMarket", data);
    });
    
    socket.on("allowAccess", function(data){
        io.emit("accessMarketAllowed", data);
    });
    
    socket.on("denyAccess", function(data){
        io.emit("accessMarketDenied", data);
    });
    
    //CART SOCKETS
    
    socket.on("finishCart", function(data){
        io.emit("cartFinished", data);
    });
    
    socket.on("acceptOrder", function(data){
        io.emit("orderAccepted", data);
    });
    
    socket.on("declineOrder", function(data){
        io.emit("orderDeclined", data);
    });
});

