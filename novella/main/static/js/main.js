function mainPageViewModel() {
    var self = this;
  
    self.selectedLamp = ko.observable();
    self.selectedLampBody = ko.observable();        // for creating lamp
    self.selectedLampShade = ko.observable();       // for creating lamp
    self.onlineLampBodies = ko.observableArray();
    self.onlineLampShades = ko.observableArray();
    self.onlineLamps = ko.observableArray();

    self.lname = ko.observable();

    self.slampbody = ko.observable();
    self.slampshade = ko.observable();

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
  