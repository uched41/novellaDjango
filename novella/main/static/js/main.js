function mainPageViewModel() {
    var self = this;
  
    self.selectedLamp = ko.observable();
    self.selectedLampBody = ko.observable();        // for creating lamp
    self.selectedLampShade = ko.observable();       // for creating lamp
    self.onlineLampBodies = ko.observableArray();
    self.onlineLampShades = ko.observableArray();
    self.onlineLamps = ko.observableArray();

    self.lname = ko.observable();           // for creatig lamp

    self.slampbody = ko.observable();
    self.slampshade = ko.observable();

    self.selectedCommand = ko.observable();
    self.allCommands = ko.observableArray([
        "Start display",
        "Stop display",
        "Send image",
        "Set motor speed",
        "Set cold led brightness",
        "Set warm led brightness",
    ])

    self.arg1Options = ko.observableArray();
    self.arg1Val = ko.observable();
    self.arg1Cap = ko.observable();
    self.arg1State = ko.observable(false);
    self.arg2Options = ko.observableArray();
    self.arg2Val = ko.observable();
    self.arg2Cap = ko.observable();
    self.arg2State = ko.observable(false);

    self.getOnlineLampBodies = function(){
        data = {
            command: "get_online_lampbodies"
        }
        $.post("/main/command", data).done(function(data){
            if(data.data.length > 0){
                console.log(data);
                self.onlineLampBodies(data.data);
            }
        })
    }

    self.getOnlineLampShades = function(){
        data = {
            command: "get_online_lampshades"
        }
        $.post("/main/command", data).done(function(data){
            if(data.data.length > 0){
                console.log(data);
                self.onlineLampShades(data.data);
            }
        })
    }

    self.getDevices = function(){
        self.getOnlineLampBodies();
        self.getOnlineLampShades();
    }

    self.getOnlineLamps = function(){

        data = {
            command: "get_online_lamps"
        }
        $.post("/main/command", data).done(function(data){
            if(data.data.length > 0){
                self.onlineLamps(data.data);
            }
        })
    }
    self.getOnlineLamps();  // call on page load


    self.getLampDetails = ko.computed( function(){
        if (self.selectedLamp() === undefined){
            return;
        }
        data = {
            command: "get_lamp_details",
            lamp_name: self.selectedLamp() || " "
        }
        $.post("/main/command", data).done(function(data){
            if(data.lampbody && data.lampshade){
                self.slampbody(data.lampbody);
                self.slampshade(data.lampshade);
            }
        })
    } );


    self.makeLamp = function(){
        if (self.selectedLampBody() && self.selectedLampShade() && self.lname())
        {
            data = {
                command: "make_lamp",
                body_id: self.selectedLampBody(),
                shade_id: self.selectedLampShade(),
                lamp_name: self.lname()
            }
            console.log(data);
            $.post("/main/command", data).done(function(data){
                alert(data.msg)
            })
        }
        
    }

    // get files on lamp
    self.getFiles = function(){
        if (self.selectedLamp() === undefined){
            return;
        }
        data = {
            command: "send_command",
            lamp_name: self.selectedLamp(),
            device_type: "lampshade",
            lamp_command: "Get_Files"
        }
        $.post("/main/command", data).done(function(data){
            if(data.data){
                self.arg1Options(data.data.split(','));
            }
        })
    }


    // get images on server
    self.getImages = function (){
        data = {
            command: "get_images",
        }
        $.post("/main/command", data).done(function(data){
            if(data.data){
                self.arg1Options(data.data);
            }
        })
    }


    self.processCommand = ko.computed(function(){
        if (self.selectedCommand() === undefined){
            return;
        }

        var cmd = self.selectedCommand();
        if(cmd === "Start display"){
            self.getFiles();    // get files so user can select
            self.arg1Cap("Select File");
            self.arg1State(true);
        }
        else if (cmd === "Stop display"){
            self.arg1State(false);
            self.arg1Cap("");
            self.arg2State(false);
        }
        else if (cmd === "Set motor speed"){
            self.arg1State(true);
            self.arg1Options(["25%", "50%", "75%", "100%",]);
            self.arg1Cap("Select motor speed");
            self.arg2State(false);
        }
        else if (cmd === "Set cold led brightness"){
            self.arg1State(true);
            self.arg1Options(["25%", "50%", "75%", "100%"]);
            self.arg1Cap("Select brightness");
            self.arg2State(false);
        }
        else if (cmd === "Set warm led brightness"){
            self.arg1State(true);
            self.arg1Cap("Select brightness");
            self.arg1Options(["25%", "50%", "75%", "100%"]);
            self.arg2State(false);
        }
        else if (cmd === "Send image" ){
            self.getImages();
            self.arg1State(true);
            self.arg1Cap("Select image");
        }
    })


    // function to submit command 
    self.submit = function(){
        data = []
        data.lamp_name = self.selectedLamp();
        cmd = self.selectedCommand();

        if (cmd == "Start display"){
            data.command = "send_command";
            data.device_type = "lampshade";
            temp = {
                command: "Start_Display",
                file: self.arg1Val(),
            }
            data.lamp_command = JSON.stringify(temp);
        }

        else if (cmd == "Stop display"){
            data.command = "send_command";
            data.device_type = "lampshade";
            temp = { command: "Stop_Display", }
            data.lamp_command = JSON.stringify(temp);
        }

        else if (cmd == "Set motor speed"){
            data.command = "send_command";
            data.device_type = "lampbody";
            temp = { command: "Set_Motor_Speed", value: self.arg1Val(), }
            data.lamp_command = JSON.stringify(temp);
        }

        else if (cmd == "Set cold led brightness"){
            data.command = "send_command";
            data.device_type = "lampbody";
            temp = { command: "Set_ColdLed_Brightness", value: self.arg1Val(), }
            data.lamp_command = JSON.stringify(temp);
        }

        else if (cmd == "Set warm led brightness"){
            data.command = "send_command";
            data.device_type = "lampbody";
            temp = { command: "Set_WarmLed_Brightness", value: self.arg1Val(), }
            data.lamp_command = JSON.stringify(temp);
        }

        else if( cmd == "Send image"){
            data.command = "send_image";
            data.image_name = self.arg1Val();
        }
        console.log(data);

        $.post("/main/command", data).done(function(data){
            alert(data);
        })
    }

    self.upload = function(){

    }


    // get online lamps every 5 seconds
    let timer = setInterval(function() {
        self.getOnlineLamps();
      }, 5000);

  }
  
  /* On Document ready: Initialization */
  $(document).ready(function() {
      
    ko.applyBindings(
      new mainPageViewModel(),
      document.getElementById("mainCont")
    );
  });
  