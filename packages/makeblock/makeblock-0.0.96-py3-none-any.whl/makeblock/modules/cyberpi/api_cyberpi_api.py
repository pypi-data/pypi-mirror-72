# Automatic file, do not edit!

module_auto = None
board = None
import time
from . import BaseModuleAuto
from makeblock.protocols.PackData import HalocodePackData

def autoconnect():
    global module_auto
    if module_auto is None:
        module_auto = BaseModuleAuto(board)
        # blocking to wait cyberpi start  
        board.broadcast()
        # go into online mode
        board.call(HalocodePackData.broadcast())


def goto_offline_mode():
    autoconnect()
    board.call(HalocodePackData([0xf3, 0xf6, 0x03, 0x0, 0x0d, 0x0, 0x00, 0x0e, 0xf4]))

def goto_online_mode():
    autoconnect()
    board.call(HalocodePackData([0xf3, 0xf6, 0x03, 0x0, 0x0d, 0x0, 0x01, 0x0e, 0xf4]))


def set_recognition_url(server = 1, url = "http://msapi.passport3.makeblock.com/ms/bing_speech/interactive"): 
    autoconnect()
    return module_auto.common_request("be139ea20b00673e9e8dcb7bc1640df9", (server , url ))

def get_mac_address():
    autoconnect()
    return module_auto.common_request("79b023fb7e007b2291a54784c3ab045f", () ,30)

def get_battery():
    autoconnect()
    return module_auto.get_value("3988e0aab4777855379065fc8da2ba34", ())

def get_firmware_version():
    autoconnect()
    return module_auto.common_request("84130d80d8bd240c93e5809565d4fb93", () ,30)

def get_ble():
    autoconnect()
    return module_auto.common_request("3636689f7387305b262ef85f68736204", () ,30)

def get_name():
    autoconnect()
    return module_auto.common_request("974853ae311b0874fd141e4dbc7ea504", () ,30)

def set_name(name):
    autoconnect()
    return module_auto.common_request("3d43914582aed35b01093bddb465dc5a", (name) ,30)

def get_brightness():
    autoconnect()
    return module_auto.get_value("69d00a7b2ddc1d85e7ed380663f01ecf", ())

def get_bri():
    autoconnect()
    return module_auto.get_value("04eeffd3a88cf7eee2bf0cb141518cfd", ())

def get_loudness(mode = "maximum"):  
    autoconnect()
    return module_auto.get_value("2469bdefeb4529102292af589e8a2efc", (mode ))

def is_tiltback():
    autoconnect()
    return module_auto.get_value("4cf92569435ea2828f6e3b6304907430", ())

def is_tiltforward():
    autoconnect()
    return module_auto.get_value("aeefd935140b9ce16ede5da7b7ada9fa", ())

def is_tiltleft():
    autoconnect()
    return module_auto.get_value("a4cf641a79cf925a87725098646118f9", ())

def is_tiltright():
    autoconnect()
    return module_auto.get_value("fec52f5ad18094161cec1b417c7e10f5", ())

def is_faceup():
    autoconnect()
    return module_auto.get_value("43c455ca4f76e8a737618fbef054bdbe", ())

def is_facedown():
    autoconnect()
    return module_auto.get_value("c6830cf56b1a4f9aaee9ab53e89a923d", ())

def is_stand():
    autoconnect()
    return module_auto.get_value("c1fb2bd86ac930a853470c2e99c81ea2", ())

def is_handstand():
    autoconnect()
    return module_auto.get_value("c6d9801ca9be3f1032f2be41538fa658", ())

def is_shake():
    autoconnect()
    return module_auto.get_value("c33fcd8e57ae1e3b4c513f6f3386b4b6", ())

def is_waveup():
    autoconnect()
    return module_auto.get_value("e880c1ca448156bf3f371490414e4ee8", ())

def is_wavedown():
    autoconnect()
    return module_auto.get_value("aefc483bd0bcd4561ee6d6d2abface7c", ())

def is_waveleft():
    autoconnect()
    return module_auto.get_value("2dd513e5fbaf94cfe7cafdc64ebbeb74", ())

def is_waveright():
    autoconnect()
    return module_auto.get_value("231b8c48c8b30f532899415153ce868e", ())

def is_freefall():
    autoconnect()
    return module_auto.get_value("dfabbe0e342dffec53fedfff55bff3e1", ())

def is_clockwise():
    autoconnect()
    return module_auto.get_value("fe32241d6feac2a268f7eafa488761eb", ())

def is_anticlockwise():
    autoconnect()
    return module_auto.get_value("196145516d82a638b39657e5b657df7c", ())

def get_shakeval():
    autoconnect()
    return module_auto.get_value("8a5db13c5c596e0407aa4abbe4f1db48", ())

def get_wave_angle():
    autoconnect()
    return module_auto.get_value("1632d0eb591aed54c5762a5dcdab81ed", ())

def get_wave_speed():
    autoconnect()
    return module_auto.get_value("822687ed58d16f303cc79e0b03bb6ce4", ())

def get_roll():
    autoconnect()
    return module_auto.get_value("1ff145c62ee8412c628e0b0a16fd67fc", ())

def get_pitch():
    autoconnect()
    return module_auto.get_value("36119451128173ff12497681ec2502e4", ())

def get_yaw():
    autoconnect()
    return module_auto.get_value("6bc201e4c360195c6ef04a99c3adb982", ())

def reset_yaw():
    autoconnect()
    return module_auto.common_request("8f4ae00969ac36f47100a06eee0d5046", () ,30)

def get_acc(axis):
    autoconnect()
    return module_auto.get_value("c9f33e1c6b89d173924779a21a9b1019", (axis))

def get_gyro(axis):
    autoconnect()
    return module_auto.get_value("55ddb68e0c157494d0f7e9825815ed43", (axis))

def get_rotation(axis):
    autoconnect()
    return module_auto.get_value("57f3a0363bf3394221b09dd8c8667892", (axis))

def reset_rotation(axis= "all"):
    autoconnect()
    return module_auto.common_request("2e150de47aabc09be2cd468491e39a37", (axis) ,30)



class controller_c():

    def is_press(self, name):
        autoconnect()
        return module_auto.get_value("0f4008600f10c30d9500bf0896cb3945", ( name))

    def get_count(self, name):
        autoconnect()
        return module_auto.get_value("f57ae52200b5f46041c7804eec7e0423", ( name))

    def reset_count(self, name):
        autoconnect()
        return module_auto.common_request("87aca6f56a1f74eab8abb4c29616ad3c", ( name) ,30)

controller=controller_c()


class audio_c():

    def play(self, music_name):
        autoconnect()
        return module_auto.common_request("99350cd953df88e5f025bcef34113717", ( music_name) ,30)

    def play_until(self, music_name):
        autoconnect()
        return module_auto.common_request("0fd6e3524a5e7c70ccb4ae7194c3ebd4", ( music_name) ,30)

    def record(self):
        autoconnect()
        return module_auto.common_request("8bd7053a4dd190e81637918be72deb46", () ,30)

    def stop_record(self):
        autoconnect()
        return module_auto.common_request("e5e11eee2dfa73a8626ad875188ce3ca", () ,30)

    def play_record_until(self):
        autoconnect()
        return module_auto.common_request("7e7984879e15188bbc90283564d6bdf5", () ,30)

    def play_record(self):
        autoconnect()
        return module_auto.common_request("a8d3656533d5343390a4545985c40c5d", () ,30)

    def play_tone(self, freq, t = None):
        autoconnect()
        return module_auto.common_request("611cfa431119957e2345e9db178252c6", ( freq, t ) ,30)

    def play_drum(self, type, beat):
        autoconnect()
        return module_auto.common_request("db5f575f0e9b43a42505970665e7f263", ( type, beat) ,30)

    def play_music(self, note, beat, type = "piano"):
        autoconnect()
        return module_auto.common_request("3a5b01ef1cc7cf8d5eb05aa275ab0d3f", ( note, beat, type ) ,30)

    def play_note(self, note, beat):
        autoconnect()
        return module_auto.common_request("487b1f0a257ab4cad6edd09ea1df35a0", ( note, beat) ,30)

    def add_tempo(self, pct):
        autoconnect()
        return module_auto.common_request("7cf9bc83ad4148ac607d266d30a4d873", ( pct) ,30)

    def set_tempo(self, pct):
        autoconnect()
        return module_auto.common_request("97f80d0c8e36537051d6c9b21e8a7e56", ( pct) ,30)

    def get_tempo(self):
        autoconnect()
        return module_auto.common_request("0b4dbd2d04bdaac5cf2f578c6087d58d", () ,30)

    def add_vol(self, val):
        autoconnect()
        return module_auto.common_request("f4b0497ab889a85a865a7486dc9c3b20", ( val) ,30)

    def set_vol(self, val):
        autoconnect()
        return module_auto.common_request("c2e5e981c561ba61d2d757a61ff17baa", ( val) ,30)

    def get_vol(self):
        autoconnect()
        return module_auto.common_request("4dedceaadf514a624dea51612e1d3f31", () , 30)

    def stop(self):
        autoconnect()
        return module_auto.common_request("510b2145fdd0714503879cc98c435d81", () , 30)

audio=audio_c()


class display_c():

    def set_brush(self, r = 0, g = 0, b = 0):
        autoconnect()
        return module_auto.common_request("3b6fa373ef8ec0614b60949d7a6498eb", ( r , g , b ) , 30    )

    def set_title_color(self, r = 0, g = 0, b = 0):
        autoconnect()
        return module_auto.common_request("f5d5d6501e3afd18d87e81b0ec5eadb4", ( r , g , b ) , 30)

    def rotate_to(self, angle):
        autoconnect()
        return module_auto.common_request("702530b11223d816f2a79852a5298b7c", ( angle) ,30)

    def clear(self):
        autoconnect()
        return module_auto.common_request("91aee200649793797d3c8194f3c9e751", () ,30    )

    def off(self):
        autoconnect()
        return module_auto.common_request("064b32a98954fee5dba9c08ce8e9ad37", () , 30)

    def label(self, message, size, x = 0, y = 0, new_flag = False):
        autoconnect()
        return module_auto.common_request("2b099ea04f7109e654b4556d98c89caa", ( message, size, x , y , new_flag ) ,30)

    def show_label(self, message, size, x = 0, y = 0, new_flag = False):
        autoconnect()
        return module_auto.common_request("e3d7894d178c918ae0d4ec9dc34c4765", ( message, size, x , y , new_flag ) ,30)

display=display_c()


class console_c():

    def clear(self):
        autoconnect()
        return module_auto.common_request("dbeeb276871d7a91b2466c5fc9c02222", () ,30)

    def print(self, message):
        autoconnect()
        return module_auto.common_request("5d64cc86824e28e871fb85902181ff18", ( message) ,30)

    def println(self, message):
        autoconnect()
        return module_auto.common_request("778c0e54274e093926b2012fa3cc6ba4", ( message) ,30)

console=console_c()


class chart_c():

    def set_name(self, name):
        autoconnect()
        return module_auto.common_request("fb465e33a0d73e1ff32e945c30f12836", ( name) , 30)

    def clear(self):
        autoconnect()
        return module_auto.common_request("e2c4c0b767853bfb5254e88235ce635b", () , 30)

chart=chart_c()


class linechart_c():

    def add(self, data):
        autoconnect()
        return module_auto.common_request("9c7c0606827e5299122c6b71119a8bab", ( data) ,30    )

    def set_step(self, step):
        autoconnect()
        return module_auto.common_request("53e2d964d0bb39fb905c5b6b63904c43", ( step) , 30)

linechart=linechart_c()


class barchart_c():

    def add(self, data):
        autoconnect()
        return module_auto.common_request("953af5bbd66750092d3a1406d53399f3", ( data) ,30 )

barchart=barchart_c()


class table_c():

    def add(self, row, column, data):
        autoconnect()
        return module_auto.common_request("2516ef92512360a0c5a7cb54cfa30d7d", ( row, column, data) ,30 )

table=table_c()


class led_c():

    def on(self, r = 0, g = 0, b = 0, id = "all"):
        autoconnect()
        return module_auto.common_request("5119428dbfeb589dac36fb628ca9248d", ( r , g , b , id ) , 30)

    def play(self, name = "rainbow"):
        autoconnect()
        return module_auto.common_request("0c6872183c51d59d859becb64667c349", ( name ) ,30)

    def show(self, color, offset = 0):
        autoconnect()
        return module_auto.common_request("c1de77fafa5b4a4e059515b451a5378d", ( color, offset ) , 30)

    def move(self, step = 1):
        autoconnect()
        return module_auto.common_request("3164e897ffb74c0994c83a84f4938989", ( step ) , 30)

    def off(self, id = "all"):
        autoconnect()
        return module_auto.common_request("883bd62fb06060130e7da7ef5eb29eb6", ( id ) , 30)

    def add_bri(self, brightness):
        autoconnect()
        return module_auto.common_request("12d6db993b5874c141e65e740383fd09", ( brightness) , 30)

    def set_bri(self, brightness):
        autoconnect()
        return module_auto.common_request("8fd93cf231967274847b712d132b2647", ( brightness) , 30)

    def get_bri(self):
        autoconnect()
        return module_auto.common_request("f32939dd291b3df36b000e28357ec849", () , 30)

led=led_c()


class wifi_c():

    def connect(self, ssid, password):
        autoconnect()
        return module_auto.common_request("bd1de88cc76a8dbff3a0adea09a34234", ( ssid, password) , 30)

    def is_connect(self):
        autoconnect()
        return module_auto.common_request("f0b19cff8669fd061bf3bf8d755a9eee", () , 30)

wifi=wifi_c()


class cloud_c():

    def setkey(self, key):
        autoconnect()
        _pack = HalocodePackData()
        _pack.type = HalocodePackData.TYPE_SCRIPT
        _pack.script = "cyberpi.driver.cloud_translate.set_token(\"" + key + "\", \"maccesstoken\")"
        _pack.on_response = module_auto.common_request_response_cb
        _pack.mode = HalocodePackData.TYPE_RUN_WITHOUT_RESPONSE
        module_auto.send_script(_pack)
        time.sleep(0.05)
        board.call(HalocodePackData([0xf3, 0x59, 0x66, 0x00, 0x28, 0x02, 0x00, 0x60, 0x00, 0x63, 0x79, 0x62, 0x65, 0x72, 0x70, 0x69, 0x2e, 0x64, 0x72, 0x69, 0x76, 0x65, 0x72, 0x2e, 0x63, 0x6c, 0x6f, 0x75, 0x64, 0x5f, 0x74, 0x72, 0x61, 0x6e, 0x73, 0x6c, 0x61, 0x74, 0x65, 0x2e, 0x54, 0x52, 0x41, 0x4e, 0x53, 0x5f, 0x55, 0x52, 0x4c, 0x20, 0x3d, 0x20, 0x22, 0x68, 0x74, 0x74, 0x70, 0x3a, 0x2f, 0x2f, 0x6d, 0x73, 0x61, 0x70, 0x69, 0x2e, 0x6d, 0x61, 0x6b, 0x65, 0x62, 0x6c, 0x6f, 0x63, 0x6b, 0x2e, 0x63, 0x6f, 0x6d, 0x2f, 0x6d, 0x73, 0x2f, 0x62, 0x69, 0x6e, 0x67, 0x5f, 0x73, 0x70, 0x65, 0x65, 0x63, 0x68, 0x2f, 0x74, 0x72, 0x61, 0x6e, 0x73, 0x6c, 0x61, 0x74, 0x65, 0x22, 0xd5, 0xf4]))
        time.sleep(0.1)
        return module_auto.common_request("8161e0b45af7e1d12e2bd714b8b3d47f", ( key) , 30)

    def weather(self, option, woe_id):
        autoconnect()
        return module_auto.common_request("434de984f1ad299d904e3deb2cb002e2", ( option, woe_id) , 30)

    def air(self, option, woe_id):
        autoconnect()
        return module_auto.common_request("402dae9adbacff802492236ba6c977c2", ( option, woe_id) , 30)

    def time(self, option, location):
        autoconnect()
        return module_auto.common_request("70279bf87312616ec7e74ab28530fb32", ( option, location) , 30)

    def listen(self, language, t = 3):
        autoconnect()
        return module_auto.common_request("97adee4bd25bc6c77195451d5e7a42d6", ( language, t ) , 30    )

    def listen_result(self):
        autoconnect()
        return module_auto.common_request("10b07f3c97a2833abaeea5b42aa892b7", () , 30)

    def tts(self, language, message):
        autoconnect()
        return module_auto.common_request("093cf48163eb9ae0997ea9f6a521c2f2", ( language, message) , 30)

    def translate(self, language, message):
        autoconnect()
        return module_auto.common_request("716553fa3b4c7469133cf3d465536cd5", ( language, message) , 30)

cloud=cloud_c()


class timer_c():

    def get(self):
        autoconnect()
        return module_auto.get_value("5535075a55d873b7450bad031ba3ba72", ())

    def reset(self):
        autoconnect()
        return module_auto.common_request("e5359d1a429dbef33644fa7d5e450ab2", () , 30)

timer=timer_c()
def broadcast(message):
    autoconnect()
    return module_auto.common_request("973eab065d5f700522b11bff0540f19a", (message) , 30)

def broadcast_and_wait(message):
    autoconnect()
    return module_auto.common_request("fe662895f3ea37bdb913466a5b6ba520", (message) , 30)



class wifi_broadcast_c():

    def set(self, message, value):
        autoconnect()
        return module_auto.common_request("e0b9fb05284e48b4d7a4a97c25eca5de", ( message, value) ,30)

    def get(self, message):
        autoconnect()
        return module_auto.common_request("f125d69e4401eb06e48ccd6bb3d6c895", ( message) ,30    )

wifi_broadcast=wifi_broadcast_c()


class upload_broadcast_c():

    def set(self, message, value):
        autoconnect()
        return module_auto.common_request("71de891af2a5dcbb9a8f4ed958060137", ( message, value) ,30)

    def get(self, message):
        autoconnect()
        return module_auto.common_request("4b09d734021e25bcf990c7896f0ed816", ( message) ,30)

upload_broadcast=upload_broadcast_c()


class cloud_broadcast_c():

    def set(self, message, value):
        autoconnect()
        return module_auto.common_request("91f7a4c19cdcf0592e368049f5cb04ea", ( message, value) ,30)

    def get(self, message):
        autoconnect()
        return module_auto.common_request("d51ad9449c1a722b7df593a3ea603ee0", ( message) ,30)

cloud_broadcast=cloud_broadcast_c()


class pocket_c():

    def motor_add(self, power, port):
        autoconnect()
        return module_auto.common_request("f14cf3698d0a66c7e7dc137979208559", ( power, port) , 30)

    def motor_set(self, power, port):
        autoconnect()
        return module_auto.common_request("0bbfb936f93f376709b85ce198b36ebe", ( power, port) , 30    )

    def motor_get(self, port):
        autoconnect()
        return module_auto.common_request("d9f5ba4f16b1e646a7ee49bc4309984b", ( port) , 30    )

    def motor_drive(self, power1, power2):
        autoconnect()
        return module_auto.common_request("9709a31105debd6284eaafa028e08851", ( power1, power2) , 30)

    def motor_stop(self, port):
        autoconnect()
        return module_auto.common_request("4841509eb9dd1beffdf13d245f81c030", ( port) , 30)

    def servo_add(self, angle, port):
        autoconnect()
        return module_auto.common_request("8f7607cc42694039b9c05a92ac38d096", ( angle, port) , 30)

    def servo_set(self, angle, port):
        autoconnect()
        return module_auto.common_request("776ebb4dd454816c9109e050c4223ec4", ( angle, port) , 30)

    def servo_get(self, port):
        autoconnect()
        return module_auto.common_request("be36631cd53eaf910c4e9070ac09ec27", ( port) , 30)

    def servo_release(self, port):
        autoconnect()
        return module_auto.common_request("42fb7c303ee2d34c2951128d98955f37", ( port) , 30)

    def servo_drive(self, angle1, angle2):
        autoconnect()
        return module_auto.common_request("11e6a43ca3a2eaf8ba8925cbf4a0b9a1", ( angle1, angle2) , 30)

    def led_on(self, r = 0, g = 0, b = 0, id = 1, port = 'S1'):
        autoconnect()
        return module_auto.common_request("dec8a1a20537cde484678e9cfeed4ff5", ( r , g , b , id , port ) , 30)

    def led_show(self, color, port):
        autoconnect()
        return module_auto.common_request("d963c1df3f3bf425ce3a54941ec6eb1b", ( color, port) , 30)

    def led_move(self, step, cycle, port):
        autoconnect()
        return module_auto.common_request("8e5a4f975d3655c574cd88b74a775d43", ( step, cycle, port) , 30)

    def led_off(self, id = 'all', port = 'S1'):
        autoconnect()
        return module_auto.common_request("a2155c2883e4ade480316b26a29d3841", ( id , port ) , 30)

    def led_add_bri(self, brightness, port):
        autoconnect()
        return module_auto.common_request("34c16d2f099b94f7399869a4baa24ee7", ( brightness, port) , 30)

    def led_set_bri(self, brightness, port):
        autoconnect()
        return module_auto.common_request("201d614cd682f60391f4af94c8784910", ( brightness, port) , 30)

    def led_get_bri(self, port):
        autoconnect()
        return module_auto.common_request("828e20bbbe7048388e0f991ea7d75743", ( port) ,30)

    def write_digital(self, val, port):
        autoconnect()
        return module_auto.common_request("d798a5bda868c3cf30fe9015dc758384", ( val, port) , 30)

    def read_digital(self, port):
        autoconnect()
        return module_auto.common_request("604ffb911872fb6f62907f266b35c31c", ( port) ,30)

    def set_pwm(self, duty, frequency, port):
        autoconnect()
        return module_auto.common_request("718a577e169f580a16dd6ac78a4a270a", ( duty, frequency, port) , 30)

    def read_analog(self, port):
        autoconnect()
        return module_auto.common_request("cc75739dc5143b3863dcfa023a33fc06", ( port) ,30)

pocket=pocket_c()


class button_c():

    def is_press(self, index = 1):
        autoconnect()
        return module_auto.get_value("2fd7fdd9cc364e93839af5093eccada0", ( index ))

    def get_count(self, index = 1):
        autoconnect()
        return module_auto.get_value("6036b0c4c2a8de19dcfe66bc771b708f", ( index ))

    def reset_count(self, index = 1):
        autoconnect()
        return module_auto.common_request("4d3d6225ee7b02a374f7d6d9902d59e5", ( index ) ,30)

button=button_c()


class angle_sensor_c():

    def get(self, index = 1):
        autoconnect()
        return module_auto.get_value("466a0a7e36e2f0833c8f9712dc1347da", ( index ))

    def reset(self, index = 1):
        autoconnect()
        return module_auto.common_request("d357c560efdea10412a3fd77b6e7407d", ( index ) ,30)

    def get_speed(self, index = 1):
        autoconnect()
        return module_auto.get_value("653c264f992c745f19595f198e366064", ( index ))

    def is_clockwise(self, index = 1):
        autoconnect()
        return module_auto.get_value("74beee720507e4f16fcf069e8258ff1b", ( index ))

    def is_anticlockwise(self, index = 1):
        autoconnect()
        return module_auto.get_value("767a7284b254922aac50bb54b3304af9", ( index ))

angle_sensor=angle_sensor_c()


class slider_c():

    def get(self, index = 1):
        autoconnect()
        return module_auto.get_value("4218158c5f90b52093f9b633567028cb", ( index ))

slider=slider_c()


class joystick_c():

    def get_x(self, index = 1):
        autoconnect()
        return module_auto.get_value("329b0ec2001972b145f60dac9243800c", ( index ))

    def get_y(self, index = 1):
        autoconnect()
        return module_auto.get_value("3c6aa9e81a72607205a5fe22c0a7b34a", ( index ))

    def is_up(self, index = 1):
        autoconnect()
        return module_auto.get_value("d26cf2d9b787ce3f50582ad3e9683c91", ( index ))

    def is_down(self, index = 1):
        autoconnect()
        return module_auto.get_value("6e41766690b2a7a76a45a5fc83075707", ( index ))

    def is_left(self, index = 1):
        autoconnect()
        return module_auto.get_value("702ed21aa14e43084db76801d297c1e9", ( index ))

    def is_right(self, index = 1):
        autoconnect()
        return module_auto.get_value("7c08a552c6941671baf17b4760ba3b9a", ( index ))

joystick=joystick_c()


class multi_touch_c():

    def is_touch(self, ch = 'any', index = 1):
        autoconnect()
        return module_auto.get_value("7dc6c2793ae0b47221c01421cc493a90", ( ch , index ))

    def set(self, level = "middle", index = 1):
        autoconnect()
        return module_auto.common_request("7996e1354d54932fc066fbbfd4cd58c5", ( level , index ) ,30)

    def reset(self, level = "middle", index = 1):
        autoconnect()
        return module_auto.common_request("bc19c76773a823bcd72b6a3cc3bf64d2", ( level , index ) ,30)

multi_touch=multi_touch_c()


class light_sensor_c():

    def get(self, index = 1):
        autoconnect()
        return module_auto.get_value("61a4e7daeb90a389e55f49cd52da3087", ( index ))

light_sensor=light_sensor_c()


class dual_rgb_sensor_c():

    def get_red(self, ch = 1, index = 1):
        autoconnect()
        return module_auto.get_value("0a4a48ee6c3a39125e3bcc4d22b61bd9", ( ch , index ))

    def get_green(self, ch = 1, index = 1):
        autoconnect()
        return module_auto.get_value("ec148aee5faa180529bdd9ae1b6fb769", ( ch , index ))

    def get_blue(self, ch = 1, index = 1):
        autoconnect()
        return module_auto.get_value("89c4a7530f4dd5c02d45df34c9c1e99d", ( ch , index ))

    def is_color(self, color = 'white', ch = 1, index = 1):
        autoconnect()
        return module_auto.get_value("11fc67e6b3a0491c133e63ee203d67b0", ( color , ch , index ))

    def get_light(self, ch = 1, index = 1):
        autoconnect()
        return module_auto.get_value("47599c2d9bc858c9da8eb95b8082a12b", ( ch , index ))

    def get_gray_level(self, ch = 1, index = 1):
        autoconnect()
        return module_auto.get_value("21529a6b724230b961b667fd22e4b0d9", ( ch , index ))

    def set_led(self, color = 'white', index = 1):
        autoconnect()
        return module_auto.common_request("94ecd63bfd0ded6367f78cac36147008", ( color , index ) , 30)

    def off_led(self, index = 1):
        autoconnect()
        return module_auto.common_request("8acfd8aef4f03c2c405cff8d10d850a0", ( index ) , 30   )

dual_rgb_sensor=dual_rgb_sensor_c()


class sound_sensor_c():

    def get(self, index = 1):
        autoconnect()
        return module_auto.get_value("4803135ff11d9ddf810a4558215d3c05", ( index ))

sound_sensor=sound_sensor_c()


class pir_c():

    def is_detect(self, index = 1):
        autoconnect()
        return module_auto.get_value("33adf300e6cf16c79c42d51ef4138434", ( index ))

    def get_count(self, index = 1):
        autoconnect()
        return module_auto.get_value("637f77cf83a15fb73181d8248d2209f8", ( index ))

    def reset_count(self, index = 1):
        autoconnect()
        return module_auto.common_request("8ad1d67e0b59f87a4deb3750b6b1898c", ( index ) ,30    )

pir=pir_c()


class ultrasonic_c():

    def get(self, index = 1):
        autoconnect()
        return module_auto.get_value("53b508a9d07ca4ea6fdc127746f26353", ( index ))

ultrasonic=ultrasonic_c()


class ranging_sensor_c():

    def get(self, index = 1):
        autoconnect()
        return module_auto.get_value("336a80558295423ce35698210a1314c9", ( index ))

ranging_sensor=ranging_sensor_c()


class motion_sensor_c():

    def is_tiltleft(self, index = 1):
        autoconnect()
        return module_auto.get_value("cb3a28f5868da4a112215c0c2d0cd80e", ( index ))

    def is_tiltright(self, index = 1):
        autoconnect()
        return module_auto.get_value("1b50341ddeac7bdfe6a70b6d0326e703", ( index ))

    def is_tiltup(self, index = 1):
        autoconnect()
        return module_auto.get_value("07aba7578dc5725e307cc0d6473f1519", ( index ))

    def is_tiltdown(self, index = 1):
        autoconnect()
        return module_auto.get_value("2ae39725fb057646d13496e3451541c9", ( index ))

    def is_faceup(self, index = 1):
        autoconnect()
        return module_auto.get_value("9915f25af1ad344d6acb3b4f9a669c3b", ( index ))

    def is_facedown(self, index = 1):
        autoconnect()
        return module_auto.get_value("236094366aec9449878d5242bc4c6d64", ( index ))

    def is_shake(self, index = 1):
        autoconnect()
        return module_auto.get_value("26c0ae50fe1701d6489a197a71e3613f", ( index ))

    def get_shakeval(self, index = 1):
        autoconnect()
        return module_auto.get_value("5cc3f3c28bd844b90f44f194ad7650cf", ( index ))

    def get_accel(self, axis, index = 1):
        autoconnect()
        return module_auto.get_value("7a29c6c9ccb4772f95539b22d1e4889e", ( axis, index ))

    def get_gyro(self, index = 1):
        autoconnect()
        return module_auto.get_value("a0a6c73408a7358641fbc419b703e51d", ( index ))

    def get_roll(self, index = 1):
        autoconnect()
        return module_auto.get_value("9c1816917b4f5c2488fcc98898cf9800", ( index ))

    def get_pitch(self, index = 1):
        autoconnect()
        return module_auto.get_value("bf545bd2aead7ec5841b1ae355433fa1", ( index ))

    def get_yaw(self, index = 1):
        autoconnect()
        return module_auto.get_value("02ec9ecd2e720e53f308d71ad809ec04", ( index ))

    def get_rotation(self, index = 1):
        autoconnect()
        return module_auto.get_value("066e7834857a4070facfb0baf6b344da", ( index ))

    def reset_rotation(self, index = 1):
        autoconnect()
        return module_auto.common_request("8c5f098af82a67337f2aa2965872878a", ( index ) ,30  )

motion_sensor=motion_sensor_c()


class soil_sensor_c():

    def get(self, index = 1):
        autoconnect()
        return module_auto.get_value("6729612451f44c7d9e968c5bb183380a", ( index ))

soil_sensor=soil_sensor_c()


class temp_sensor_c():

    def get(self, index = 1):
        autoconnect()
        return module_auto.get_value("8a7a5671b5bfbe8581afabbea4b28064", ( index ))

temp_sensor=temp_sensor_c()


class humiture_c():

    def get_humidity(self, index = 1):
        autoconnect()
        return module_auto.get_value("cb1d9f1546082a8fa7d5d3b7d39691dc", ( index ))

    def get_temp(self, index = 1):
        autoconnect()
        return module_auto.get_value("37663d09a8728687d7dae5938ec173fe", ( index ))

humiture=humiture_c()


class mq2_c():

    def is_detect(self, level = 'high',index = 1):
        autoconnect()
        return module_auto.get_value("c4ca0e449ec7efbbc2867ccb25972fdb", ( level ,index ))

    def get(self, index = 1):
        autoconnect()
        return module_auto.get_value("8e5afd5fb157dd54f831e29126bd1dac", ( index ))

mq2=mq2_c()


class flame_sensor_c():

    def is_detect(self, index = 1):
        autoconnect()
        return module_auto.get_value("fdf535e5437a3f63b1c53497cb0bf6e6", ( index ))

    def get(self, index = 1):
        autoconnect()
        return module_auto.get_value("3918994d8aa93f4b108b29914a5a9c2f", ( index ))

flame_sensor=flame_sensor_c()


class magnetic_sensor_c():

    def is_detect(self, index = 1):
        autoconnect()
        return module_auto.get_value("a1d01f6784d3fbdb25c9890c475fa1af", ( index ))

    def get_count(self, index = 1):
        autoconnect()
        return module_auto.get_value("a9be5788b430f72e8890e53076a45f87", ( index ))

    def reset_count(self, index = 1):
        autoconnect()
        return module_auto.common_request("514caf43affa7206b98961d67b39b2a5", ( index ) ,30 )

magnetic_sensor=magnetic_sensor_c()


class led_matrix_c():

    def show(self, image = "hi", index = 1):
        autoconnect()
        return module_auto.common_request("0a36b1142cd9c57d431cd40fcdb52a63", ( image , index ) , 30)

    def show_at(self, image = "hi", x = 0, y = 0, index = 1):
        autoconnect()
        return module_auto.common_request("0a4f300dd408e4907a88dbc26bdf862a", ( image , x , y , index ) , 30)

    def print(self, message, index = 1):
        autoconnect()
        return module_auto.common_request("39aada5160f5d18f80c0a54d650f8c34", ( message, index ) , 30)

    def print_until_done(self, message, index = 1):
        autoconnect()
        return module_auto.common_request("4fc8f6ed7492088f3c3e370cdea18fee", ( message, index ) ,30 )

    def print_at(self, message, x = 0, y = 0, index = 1):
        autoconnect()
        return module_auto.common_request("fe1474ef0739be5d937398d958f3dfd0", ( message, x , y , index ) , 30)

    def on(self, x = 0, y = 0, index = 1):
        autoconnect()
        return module_auto.common_request("9cbb10b41f3f5d048cf288a9ddcaf41f", ( x , y , index ) , 30)

    def off(self, x = 0, y = 0, index = 1):
        autoconnect()
        return module_auto.common_request("6e4d10fcd4896f23af930ec3c5da811e", ( x , y , index ) , 30)

    def toggle(self, x = 0, y = 0, index = 1):
        autoconnect()
        return module_auto.common_request("13be3cd3d99e375098a47eb4f27a641f", ( x , y , index ) , 30)

    def get(self, x = 0, y = 0, index = 1):
        autoconnect()
        return module_auto.common_request("fc7e4f7e6d6d38732780cf9cb92882e4", ( x , y , index ) , 30)

    def clear(self, index = 1):
        autoconnect()
        return module_auto.common_request("2266736814ffa6880ada32aadecba3f7", ( index ) , 30)

led_matrix=led_matrix_c()


class rgb_led_c():

    def on(self, r = 0, g = 0, b = 0, index = 1):
        autoconnect()
        return module_auto.common_request("c5b5ca3035fe0e8e928cd4f77abf3136", ( r , g , b , index ) , 30)

    def off(self, index = 1):
        autoconnect()
        return module_auto.common_request("dd0462307d855e7aad2b1c4d5cb92b4d", ( index ) , 30)

    def set_red(self, val, index = 1):
        autoconnect()
        return module_auto.common_request("73ebb52c77427ea8e302214bb9f03e7d", ( val, index ) , 30)

    def set_green(self, val, index = 1):
        autoconnect()
        return module_auto.common_request("3ed525ae3a3fb8c4c3d99ce38159ab12", ( val, index ) , 30)

    def set_blue(self, val, index = 1):
        autoconnect()
        return module_auto.common_request("e7d5243d81bb07178476fd5b138132ed", ( val, index ) , 30)

    def add_red(self, val, index = 1):
        autoconnect()
        return module_auto.common_request("32d74e7fc72a8b8d368c56544525b1f8", ( val, index ) , 30)

    def add_green(self, val, index = 1):
        autoconnect()
        return module_auto.common_request("8b37c95d064ca1de35a143bb1c7cf988", ( val, index ) , 30)

    def add_blue(self, val, index = 1):
        autoconnect()
        return module_auto.common_request("353325d9328194c8808750c8ebbe7574", ( val, index ) , 30)

    def get_red(self, index = 1):
        autoconnect()
        return module_auto.common_request("f5a3ca4d2df5fe90db4adce91b6aa20a", ( index ) ,30 )

    def get_green(self, index = 1):
        autoconnect()
        return module_auto.common_request("771d65f5e53a13009bfc0d5d39b8e4e8", ( index ) ,30 )

    def get_blue(self, index = 1):
        autoconnect()
        return module_auto.common_request("519688ecd9013344908dc499a3f3119d", ( index ) ,30 )

rgb_led=rgb_led_c()


class led_driver_c():

    def on(self, r = 0, g = 0, b = 0, id = "all", index = 1):
        autoconnect()
        return module_auto.common_request("40fc880df668751be85b28ab7c866a26", ( r , g , b , id , index ) , 30)

    def off(self, id = "all", index = 1):
        autoconnect()
        return module_auto.common_request("d9fc3c5cc6dfccb58fa6df5aed1c4d96", ( id , index ) , 30)

    def set_red(self, val, id = "all", index = 1):
        autoconnect()
        return module_auto.common_request("a437fec37c65f9a8782cffce9db6bd1e", ( val, id , index ) , 30)

    def set_green(self, val, id = "all", index = 1):
        autoconnect()
        return module_auto.common_request("0fca0243087084fec4033bc78f502398", ( val, id , index ) , 30)

    def set_blue(self, val, id = "all", index = 1):
        autoconnect()
        return module_auto.common_request("33810988a6530c3d432ea8ad0cc96776", ( val, id , index ) , 30)

    def add_red(self, val, id = "all", index = 1):
        autoconnect()
        return module_auto.common_request("d9ae3f9c820e0775b45f62a3aca40bc2", ( val, id , index ) , 30)

    def add_green(self, val, id = "all", index = 1):
        autoconnect()
        return module_auto.common_request("62516697866c2a740bfdb32a810ba2f0", ( val, id , index ) , 30)

    def add_blue(self, val, id = "all", index = 1):
        autoconnect()
        return module_auto.common_request("2be3b01fe53c485e0d0eb80c8544561d", ( val, id , index ) , 30)

    def set_mode(self, mode = "steady", index = 1):
        autoconnect()
        return module_auto.common_request("679267a195b346e01bc94ac005e4e735", ( mode , index ) , 30)

    def show(self,color, index = 1):
        autoconnect()
        return module_auto.common_request("e820d887deeeb8b1b4cec6f9b1a22c77", (color, index ) , 30)

led_driver=led_driver_c()


class servo_driver_c():

    def set(self, angle, index = 1):
        autoconnect()
        return module_auto.common_request("599a9d0aaeae8af163b572258b842299", ( angle, index ) , 30)

    def add(self, angle, index = 1):
        autoconnect()
        return module_auto.common_request("24634711504cff12ed674d3817bf2669", ( angle, index ) , 30 )

    def get(self, index = 1):
        autoconnect()
        return module_auto.common_request("d6cd64b1fd1733f66a17240097819f38", ( index ) ,30     )

    def get_load(self, index = 1):
        autoconnect()
        return module_auto.common_request("a70fe6d7eed8e3fb23f624ede018c1f2", ( index ) ,30 )

    def release(self, index = 1):
        autoconnect()
        return module_auto.common_request("2b0020324c91fa7e5dcb1a738190f293", ( index ) , 30 )

servo_driver=servo_driver_c()


class motor_driver_c():

    def set(self, power, index = 1):
        autoconnect()
        return module_auto.common_request("5558035e8749d8bcc350a1128787b69e", ( power, index ) , 30)

    def add(self, power, index = 1):
        autoconnect()
        return module_auto.common_request("5ca600766d7058cee7739f7a17338513", ( power, index ) , 30)

    def get(self, index = 1):
        autoconnect()
        return module_auto.common_request("ca9591623a91a8f8d196dbb31dccf7a6", ( index ) ,30     )

    def get_load(self, index = 1):
        autoconnect()
        return module_auto.common_request("4b93f6b97a5801b7cb8ca217d323e975", ( index ) ,30 )

    def stop(self, index = 1):
        autoconnect()
        return module_auto.common_request("5574099fb868a1819d4312e029a9e43b", ( index ) , 30)

motor_driver=motor_driver_c()


class speaker_c():

    def mute(self, index = 1):
        autoconnect()
        return module_auto.common_request("372733001e64f46f2ec17d7aa9238b2e", ( index ) ,30 )

    def stop(self, index = 1):
        autoconnect()
        return module_auto.common_request("553e5b2ee1f27ca3b69f3c1077cd4a9b", ( index ) ,30 )

    def set_vol(self, volume, index = 1):
        autoconnect()
        return module_auto.common_request("5e126dc66995384c55e659b3ff0b7082", ( volume, index ) , 30    )

    def add_vol(self, volime, index = 1):
        autoconnect()
        return module_auto.common_request("f56a2f368ca8828e56e35e1e18c5377a", ( volime, index ) , 30)

    def get_vol(self, index = 1):
        autoconnect()
        return module_auto.common_request("49102cec80105f7ca1a56dd997664153", ( index ) ,30     )

    def play_tone(self, frq, t = None, index = 1):
        autoconnect()
        return module_auto.common_request("7e0558574c28779fcd007636cecc0be4", ( frq, t , index ) , 30)

    def play_music(self, name, index = 1):
        autoconnect()
        return module_auto.common_request("d3bbc391371a4e7a99845969d527935f", ( name, index ) , 30)

    def play_music_until_done(self, name, index = 1):
        autoconnect()
        return module_auto.common_request("67ba91bacf4c08405663fa0a5aeadd8c", ( name, index ) ,30 )

    def is_play(self, index = 1):
        autoconnect()
        return module_auto.common_request("7e3c5f3f01d88b7665a5adb092ac18a9", ( index ) ,30 )

speaker=speaker_c()
