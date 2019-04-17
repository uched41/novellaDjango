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
 
    self.motorOn = ko.observable();
    self.brightnessMode = ko.observable();

    self.motorControl = ko.computed(function(){
        if(self.motorOn() == undefined) return;
        data = {
            command:"send_command",
            lamp_name: self.selectedLamp(),
            device_type: "lampbody",
            lamp_command: self.motorOn()?"'command':'Motor_On'":"'command':'Motor_Off'",
        }
        $.post("/command", data).done(function(data){
            alert(data.status);
        })
    })

    self.brightControl = ko.computed(function(){
        if(self.brightnessMode() == undefined) return;
        data = {
            command:"send_command",
            lamp_name: self.selectedLamp(),
            device_type: "lampshade",
            lamp_command: self.brightnessMode()?"'command':'Brightness_Mode', 'value':'1'":"'command':'Brightness_Mode', 'value':'0'",
        }
        $.post("/command", data).done(function(data){
            alert(data.status);
        })
    })

    // describes how the input for command will be displayed
    self.commandsData =  {
        Motor_speed: {
            label: "Motor speed",
            input_type: "range",
            input_class: "form-control", 
            prepend: true,
            min: 0,
            max: 100,
            select: false,
        },
        Warm_led_brightness: {
            label: "Warm led brightness",
            input_type: "range",
            input_class: "form-control", 
            prepend: true,
            min: 0,
            max: 100,
            select: false,
        },
        Cold_led_brightness: {
            label: "Cold led brightness",
            input_type: "range",
            input_class: "form-control", 
            prepend: true,
            min: 0,
            max: 100,
            select: false,
        },
        Delete_file: {
            select: true,
            label: "Select file to delete from server",
        },
        Start_display: {
            select: true,
            label: "Select file to start",
            caption: "Select file",
        },
        Stop_display: {
            select: true,
            label: "Stop display",
        },
        Delete_bin_File: {
            select: true,
            label: "Select file to delete from master",
            caption: "Select file",
        },
        Send_image: {
            select: true,
            label: "Select image to send to lamp",
            caption: "Select file",
        },
        Image_brightness: {
            label: "Global brightness",
            input_type: "range",
            input_class: "form-control", 
            prepend: true,
            min: 1,
            max: 100,
            select: false,
        },
        Divider: {
            label: "Color divider",
            input_type: "range",
            input_class: "form-control", 
            prepend: true,
            min: 1,
            max: 128,
            select: false,
        },
        Column_delay: {
            label: "Image stretching",
            input_type: "range",
            input_class: "form-control", 
            prepend: true,
            min: 1,
            max: 500,
            select: false,
        },
    };
    
    // command options to select
    self.allCommands = ko.observableArray(Object.keys(self.commandsData));

    // Data of current command being displayed
    self.ccData = ko.observable(0);

    // selected command
    self.selectedCommand = ko.observable();

    self.arg1Options = ko.observableArray();
    self.arg1Val = ko.observable(50);
    self.arg1ValStr = ko.computed(function(){ return'' + self.arg1Val(); });
    self.arg1Cap = ko.observable();
    self.arg1State = ko.observable(true);
    self.arg1Checked = ko.observable(false);

    self.arg2Options = ko.observableArray();
    self.arg2Val = ko.observable(50);
    self.arg2State = ko.observable(true);
    

    self.getOnlineLampBodies = function(){
        data = {
            command: "get_online_lampbodies"
        }
        $.post("/command", data).done(function(data){
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
        $.post("/command", data).done(function(data){
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
        $.post("/command", data).done(function(data){
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
        $.post("/command", data).done(function(data){
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
            $.post("/command", data).done(function(data){
                alert(data.msg);
                $('#lampForm').modal('toggle');
            })
        }
        
    }

    self.deleteLamp = function(){
        data = {
            command: "delete_lamp",
            lamp_name: self.selectedLamp()
        }
        console.log(data);
        $.post("/command", data).done(function(data){
            window.location = "/main"
        })
        
        
    }

    // get files on lamp
    self.getFiles = function(){
        if (self.selectedLamp() === undefined){
            return;
        }
		temp = {command: "Get_Files"};
        data = {
            command: "send_command",
            lamp_name: self.selectedLamp(),
            device_type: "lampshade",
            lamp_command: JSON.stringify(temp)
        }
        $.post("/command", data).done(function(data){
			console.log(data)
            if(data.data){
                self.arg2Options(data.data.split(','));
            }
			else{
				self.arg2Options([]);
			}
        })
    }

    // get images on server
    self.getImages = function (){
        data = {
            command: "get_images",
        }
        $.post("/command", data).done(function(data){
            if(data.data){
                self.arg2Options(data.data);
            }
        })
    }


	self.refresh = function(){
		console.log("refreshing options");
		var cmd = self.selectedCommand();

		if(cmd === undefined) { return ;}

		if(cmd === "Start_display" || cmd === "Delete_bin_file"){
			self.getFiles();
			self.arg2State(true);
		}
		else if (cmd === "Send_image" || cmd === "Delete_file"){
			self.getImages();
			self.arg2State(true);
		}

	}

    self.processCommand = ko.computed(function(){
        var cmd = self.selectedCommand();
        if (cmd === undefined){
            return;
        }
		
        self.ccData( self.commandsData[cmd]);
        

        if(cmd === "Start_display" || cmd === "Delete_bin_File"){
            self.getFiles();    // get files so user can select
            self.arg2State(true);
        }
        else if (cmd === "Stop_display"){
            self.arg2State(false);
        }
        else if (cmd === "Send_image" || cmd === "Delete_file"){
            self.getImages();
            self.arg2State(true);
        }
    })


    // function to submit command 
    self.submit = function(){
        data = {}
        data.lamp_name = self.selectedLamp();
        cmd = self.selectedCommand();

        if (cmd == "Start_display"){
            data.command = "send_command";
            data.device_type = "lampshade";
            temp = {
                command: "Start_Display",
                file: self.arg2Val(),
            }
            data.lamp_command = JSON.stringify(temp);
        }

        else if (cmd == "Delete_bin_File"){
            data.command = "send_command";
            data.device_type = "lampshade";
            temp = { command: "Delete_Bin", file: self.arg2Val(), }
            data.lamp_command = JSON.stringify(temp);
        }

        else if (cmd == "Stop_display"){
            data.command = "send_command";
            data.device_type = "lampshade";
            temp = { command: "Stop_Display", }
            data.lamp_command = JSON.stringify(temp);
        }

        else if (cmd == "Motor_speed"){
            data.command = "send_command";
            data.device_type = "lampbody";
            temp = { command: "Set_Motor_Speed", value: self.arg1Val(), }
            data.lamp_command = JSON.stringify(temp);
        }

        else if (cmd == "Cold_led_brightness"){
            data.command = "send_command";
            data.device_type = "lampbody";
            temp = { command: "Set_ColdLed_Brightness", value: self.arg1Val(), }
            data.lamp_command = JSON.stringify(temp);
        }

        else if (cmd == "Warm_led_brightness"){
            data.command = "send_command";
            data.device_type = "lampbody";
            temp = { command: "Set_WarmLed_Brightness", value: self.arg1Val(), }
            data.lamp_command = JSON.stringify(temp);
        }

        else if (cmd == "Image_brightness"){
            data.command = "send_command";
            data.device_type = "lampshade";
            temp = { command: "Brightness", value: self.arg1Val(), }
            data.lamp_command = JSON.stringify(temp);
        }

        else if (cmd == "Column_delay"){
            data.command = "send_command";
            data.device_type = "lampshade";
            temp = { command: "Column_Delay", value: self.arg1Val(), }
            data.lamp_command = JSON.stringify(temp);
        }

        else if (cmd == "Divider"){
            data.command = "send_command";
            data.device_type = "lampshade";
            temp = { command: "Divider", value: self.arg1Val(), }
            data.lamp_command = JSON.stringify(temp);
        }

        else if( cmd == "Send_image"){
            data.command = "send_image";
            data.image_name = self.arg2Val();
        }

        else if( cmd == "Delete_file"){
            data.command = "delete_image";
            data.image_name = self.arg2Val();
        }

        console.log(data);

        $.post("/command", data).done(function(data){
            //alert(data.status);
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
  
