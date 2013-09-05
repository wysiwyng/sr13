#define encoder0PinA 2

#define encoder0PinB 3

#define taster 4
#define output1 5
#define output2 6
#define output3 7

#define token 13000
#define pedestal 70000
#define top 125000

volatile unsigned long encoder0Pos = 0;

void setup() {

  pinMode(encoder0PinA, INPUT); 
  pinMode(encoder0PinB, INPUT); 
  pinMode(taster, INPUT);
  pinMode(output1, OUTPUT);
  pinMode(output2, OUTPUT);
  pinMode(output3, OUTPUT);
  digitalWrite(taster, HIGH);


  // encoder pin on interrupt 0 (pin 2)

  attachInterrupt(0, doEncoderA, CHANGE);

  // encoder pin on interrupt 1 (pin 3)

  attachInterrupt(1, doEncoderB, CHANGE);  

  Serial.begin (115200);

}

void loop(){  
  if(digitalRead(taster)==LOW)
  {
    encoder0Pos = 0;
    PORTD = B00010000;
    //digitalWrite(output1, LOW);
    //digitalWrite(output2, LOW);
    //digitalWrite(output3, LOW);  
  }
  else
  {
  //  if(encoder0Pos > 0 && encoder0Pos < token - 1000)   //zwischen unten und token greifen
  //  {
   //   digitalWrite(output1, LOW);
   //   digitalWrite(output2, LOW);
    //  digitalWrite(output3, HIGH);      
  //  }
    if(encoder0Pos >= token - 1500 && encoder0Pos <= token + 1500)  //token greifen
    {
      PORTD = B01010000;
      //digitalWrite(output1, LOW);
      //digitalWrite(output2, HIGH);
      //digitalWrite(output3, LOW);
    }
    //else if(encoder0Pos > token + 1000 && encoder0Pos < pedestal - 1000)  //zwischen token greifen und podest
   // {
    //  digitalWrite(output1, LOW);
    //  digitalWrite(output2, LOW);
    //  digitalWrite(output3, HIGH);         
    //}
    else if(encoder0Pos >= pedestal - 1500 && encoder0Pos <= pedestal + 1500)  //podesthöhe
    {
      PORTD = B00110000;
//      digitalWrite(output1, HIGH);
//      digitalWrite(output2, LOW);
//      digitalWrite(output3, LOW);      
    }
    //else if(encoder0Pos > pedestal + 1000 && encoder0Pos < top)  //zwischen podest und ganz oben
    //{
      //digitalWrite(output1, LOW);
      //digitalWrite(output2, LOW);
      //digitalWrite(output3, HIGH);        
    //}
    else if(encoder0Pos >= top && encoder0Pos <= top + 3000)  //ganz oben
    {
      PORTD = B01110000;
//      digitalWrite(output1, HIGH);
//      digitalWrite(output2, HIGH);
//      digitalWrite(output3, LOW);    
    }      
    else  //alles andere
    {
      PORTD = B10010000;
//      digitalWrite(output1, LOW);
//      digitalWrite(output2, LOW);
//      digitalWrite(output3, HIGH);        
    }
  }
  if(Serial.available()){
    Serial.read();
    Serial.println(encoder0Pos);
  }
}

void doEncoderA(){

  // look for a low-to-high on channel A
  if (digitalRead(encoder0PinA) == HIGH) { 

    // check channel B to see which way encoder is turning
    if (digitalRead(encoder0PinB) == LOW) {  
      encoder0Pos = encoder0Pos + 1;         // CW
    } 
    else {
      encoder0Pos = encoder0Pos - 1;         // CCW
    }
  }

  else   // must be a high-to-low edge on channel A                                       
  { 
    // check channel B to see which way encoder is turning  
    if (digitalRead(encoder0PinB) == HIGH) {   
      encoder0Pos = encoder0Pos + 1;          // CW
    } 
    else {
      encoder0Pos = encoder0Pos - 1;          // CCW
    }
  }
  //Serial.println (encoder0Pos, DEC);          
  // use for debugging - remember to comment out

}

void doEncoderB(){

  // look for a low-to-high on channel B
  if (digitalRead(encoder0PinB) == HIGH) {   

    // check channel A to see which way encoder is turning
    if (digitalRead(encoder0PinA) == HIGH) {  
      encoder0Pos = encoder0Pos + 1;         // CW
    } 
    else {
      encoder0Pos = encoder0Pos - 1;         // CCW
    }
  }

  // Look for a high-to-low on channel B

  else { 
    // check channel B to see which way encoder is turning  
    if (digitalRead(encoder0PinA) == LOW) {   
      encoder0Pos = encoder0Pos + 1;          // CW
    } 
    else {
      encoder0Pos = encoder0Pos - 1;          // CCW
    }
  }

} 

