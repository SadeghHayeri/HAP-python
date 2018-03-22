// make 4 switch relay from nodeMCU
// if wifi disconnected, switches work without problem until new connection

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>

const char* ssid = "home";
const char* password = "password";

bool connectedTOWifi = false;
bool tryConnecting = false;

ESP8266WebServer server(80);

const int NODE_COUNT = 4;

struct node {
  int switchPin;
  int relayPin;

  int currRelayState;
  int lastSwitchState;
};

node nodes[NODE_COUNT];
int freePins[8] = {D0, D1, D2, D3, D4, D5, D6, D7};

void initNodes() {
  int lastPinIndex = 0;
  for(int i = 0; i < NODE_COUNT; i++) {
    nodes[i].switchPin = freePins[lastPinIndex++];
    nodes[i].relayPin = freePins[lastPinIndex++];
    nodes[i].currRelayState = LOW;
    nodes[i].lastSwitchState = LOW;
  }
}

void setupPins() {
  for(int i = 0; i < NODE_COUNT; i++) {
    pinMode(nodes[i].switchPin, INPUT);
    pinMode(nodes[i].relayPin, OUTPUT);
  }
}

void updateRelaysState() {
  for(int i = 0; i < NODE_COUNT; i++)
    digitalWrite(nodes[i].relayPin, nodes[i].currRelayState);
}

void toggleRelay(int index) {
  nodes[index].currRelayState = (nodes[index].currRelayState == HIGH) ? LOW : HIGH;
}

void setRelay(int index, int state) {
  nodes[index].currRelayState = state;
}

void checkSwitches() {
  for(int i = 0; i < NODE_COUNT; i++) {
    int currSwitchState = digitalRead(nodes[i].switchPin);
    if(nodes[i].lastSwitchState != currSwitchState)
      toggleRelay(i);
    nodes[i].lastSwitchState = currSwitchState;
  }
}

void setup(void){
  initNodes();
  setupPins();

  Serial.begin(115200);
  Serial.println("");

  //// Wait for connection
  //while (WiFi.status() != WL_CONNECTED) {
  //  delay(500);
  //  Serial.print(".");
  //}

  ///////////////////////////////////// set
  server.on("/set/1/ON", []() {
    setRelay(0, LOW);
    server.send( 200, "text/plain", "OK" );
  });
  server.on("/set/1/OFF", []() {
    setRelay(0, HIGH);
    server.send( 200, "text/plain", "OK" );
  });

  server.on("/set/2/ON", []() {
    setRelay(1, LOW);
    server.send( 200, "text/plain", "OK" );
  });
  server.on("/set/2/OFF", []() {
    setRelay(1, HIGH);
    server.send( 200, "text/plain", "OK" );
  });

  server.on("/set/3/ON", []() {
    setRelay(2, LOW);
    server.send( 200, "text/plain", "OK" );
  });
  server.on("/set/3/OFF", []() {
    setRelay(2, HIGH);
    server.send( 200, "text/plain", "OK" );
  });

  server.on("/set/4/ON", []() {
    setRelay(3, LOW);
    server.send( 200, "text/plain", "OK" );
  });
  server.on("/set/4/OFF", []() {
    setRelay(3, HIGH);
    server.send( 200, "text/plain", "OK" );
  });
  /////////////////////////////////////////

  //////////////////////////////////////////////////////// status
  server.on("/status/1", []() {
    server.send( 200, "text/plain", String(!nodes[0].currRelayState) );
  });
  server.on("/status/2", []() {
    server.send( 200, "text/plain", String(!nodes[1].currRelayState) );
  });
  server.on("/status/3", []() {
    server.send( 200, "text/plain", String(!nodes[2].currRelayState) );
  });
  server.on("/status/4", []() {
    server.send( 200, "text/plain", String(!nodes[3].currRelayState) );
  });
  ///////////////////////////////////////////////////////////////

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void){

  if(connectedTOWifi) {
    if(WiFi.status() != WL_CONNECTED) {
      connectedTOWifi = false;
      WiFi.disconnect(true);
      Serial.println("disconnected!");
      return;
    }

    server.handleClient();
  } else {

    if(!tryConnecting) {
      Serial.print("try to connect!");
      WiFi.mode(WIFI_STA);
      WiFi.begin(ssid, password);
      tryConnecting = true;
    }

    if(WiFi.status() != WL_CONNECTED) {
      Serial.print(".");
    } else {
      tryConnecting = false;
      connectedTOWifi = true;

      Serial.println("");
      Serial.print("Connected to ");
      Serial.println(ssid);
      Serial.print("IP address: ");
      Serial.println(WiFi.localIP());

      if (MDNS.begin("esp8266"))
        Serial.println("MDNS responder started");
    }
  }
  checkSwitches();
  updateRelaysState();
}
