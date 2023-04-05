def decListToHexList(DecList):
    HexList = [format(member, '#04x') for member in DecList] 
    return HexList

def calRPM(speed, rotation='CW'):
    multiplier = 1500*4.9#166.667
    maxByte = 65535      #0xFFFF
    highBytes = int((speed * multiplier) / maxByte)
    lowBytes = int((speed * multiplier) % maxByte)
    if rotation.upper() == 'CW':
        highBytes = maxByte - highBytes
        lowBytes = maxByte - lowBytes
    return [highBytes, lowBytes]

def listToRPM(listOfDec):
    maxByte = 65536
    if listOfDec == [0, 0] :
        return [listOfDec[1], 'Pause']
    if listOfDec[0] <= 0:
        return [listOfDec[1], 'CCW']
    return [maxByte-listOfDec[1], 'CW']