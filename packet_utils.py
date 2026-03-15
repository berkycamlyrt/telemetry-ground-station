import struct


def bytesToValue(byte_array, index, length):
    if length == 4:
        return struct.unpack('<f', byte_array[index:index+length])[0]
    else:
        byte_sequence = byte_array[index:index+length]
        return int.from_bytes(byte_sequence, byteorder='big')
    

def buildPacketFromInputs(fields):
        new_packet = bytearray(78)
        new_packet[0] = bytes.fromhex("ff")[0]
        new_packet[1] = bytes.fromhex("ff")[0]
        new_packet[2] = bytes.fromhex("54")[0]
        new_packet[3] = bytes.fromhex("52")[0]

        new_packet[4] = fields["team_id"]   # team id
        new_packet[5] = fields["counter"]   # counter

        new_packet[6:10] = struct.pack('f', fields["altitude"])    # altitude
        new_packet[10:14] = struct.pack('f', fields["rocket_gps_altitude"])   # rocket gps altitude
        new_packet[14:18] = struct.pack('f', fields["rocket_latitude"])   # rocket latitude
        new_packet[18:22] = struct.pack('f', fields["rocket_longitude"])   # rocket longitude 
        new_packet[22:26] = struct.pack('f', fields["payload_gps_altitude"])   # gorev yuku gps altitude
        new_packet[26:30] = struct.pack('f', fields["payload_latitude"])   # gorev yuku latitude
        new_packet[30:34] = struct.pack('f', fields["payload_longitude"])   # gorev yuku longitude

        new_packet[46:50] = struct.pack('f', fields["gyro_x"])   # gyro x
        new_packet[50:54] = struct.pack('f', fields["gyro_y"])   # gyro y
        new_packet[54:58] = struct.pack('f', fields["gyro_z"])   # gyrp z
        new_packet[58:62] = struct.pack('f', fields["acceleration_x"])   # acc x
        new_packet[62:66] = struct.pack('f', fields["acceleration_y"])   # acc y
        new_packet[66:70] = struct.pack('f', fields["acceleration_z"])   # acc z
        new_packet[70:74] = struct.pack('f', fields["angle"])   # angle

        new_packet[74] = fields["state"] # state
        new_packet[75] = fields["crc"] # crc
        
        new_packet[76] = bytes.fromhex("0d")[0]
        new_packet[77] = bytes.fromhex("0a")[0]

        return new_packet


def parsePacket(data_packet):
    team_id = bytesToValue(data_packet, 4, 1)
    counter = bytesToValue(data_packet, 5, 1)
    altitude = bytesToValue(data_packet, 6, 4)
    rocket_gps_altitude = bytesToValue(data_packet, 10, 4)
    rocket_gps_latitude = bytesToValue(data_packet, 14, 4)
    rocket_gps_longitude = bytesToValue(data_packet, 18, 4)
    payload_rocket_gps_altitude = bytesToValue(data_packet, 22, 4)
    payload_rocket_gps_latitude = bytesToValue(data_packet, 26, 4)
    payload_rocket_gps_longitude = bytesToValue(data_packet, 30, 4)
    gyro_x = bytesToValue(data_packet, 46, 4)
    gyro_y = bytesToValue(data_packet, 50, 4)
    gyro_z = bytesToValue(data_packet, 54, 4)
    acc_x = bytesToValue(data_packet, 58, 4)
    acc_y = bytesToValue(data_packet, 62, 4)
    acc_z = bytesToValue(data_packet, 66, 4)
    angle = bytesToValue(data_packet, 70, 4)
    state = bytesToValue(data_packet, 74, 1)
    crc = bytesToValue(data_packet, 75, 1)


    labels1 = [team_id, counter, altitude, rocket_gps_altitude, rocket_gps_latitude, rocket_gps_longitude, 
               payload_rocket_gps_altitude, payload_rocket_gps_latitude, payload_rocket_gps_longitude]
    labels2 = [gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, angle, state, crc]

    labels = [labels1, labels2]     

    return labels


def packetToHexStrings(data_packet):
    first_part_byte = data_packet[:39]
    second_part_byte = data_packet[39:]

    first_part_str = ""
    second_part_str = ""

    for i in range(len(first_part_byte)):
        first_part_elt = hex(first_part_byte[i])
        second_part_elt = hex(second_part_byte[i])

        first_part_str += "[{}]".format(str(first_part_elt)[2:].upper())
        second_part_str += "[{}]".format(str(second_part_elt)[2:].upper())

    return first_part_str, second_part_str


