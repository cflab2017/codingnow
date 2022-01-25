#ifndef mwebserverhtml_h_en
#define mwebserverhtml_h_en

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html>
<head>
  <title>CODINGNOW</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv='refresh' content='5'>
    <style>
        * {
            font-size: 16px;
            font-family: Consolas, sans-serif;
        }
        textarea {
            width: 80%;
            height: 60px;
        }
    </style>
</head>
<body>
    <div style="text-align:center;display:inline-block;min-width:380px;">
    <h2>저장공간</h2>
    <!-- <p><span class="dht-heading">사용된 저장공간</span></p> -->
    <p>
      <span>
        <i class="fas fa-thermometer-half" style="color:#059e8a;"></i>
        <sup id="usedmbyte">@@USED_MBYTE@@</sup>
        <sup class="units">Mbyte / </sup>
      </span>
      <span>
        <i class="fas fa-tint" style="color:#00add6;"></i>
        <sup id="usedper">@@USED_PER@@</sup>
        <sup class="units">%</sup>
      </span>
        <form>
        <p><textarea>@@MESSAGE@@</textarea></p>
        </form>
    </p>
    </div>
    <br>

    <div style="text-align:center;display:inline-block;min-width:380px;">
    <h2>ESP32 CAM 제어</h2>
    <form method='POST' action='/' >
      <INPUT type='submit' name = 'CONTROL' value='Start'>
      <INPUT type='submit' name = 'CONTROL' value='Stop'>
    </form>
    </div>

    <br>

  <h2>ESP Image Web Server</h2>
  <img src="cam">
</body>  
</html>)rawliteral";
#endif