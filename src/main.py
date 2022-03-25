import time
import urx
import enum
import keyboard

class Modes(enum.Enum):
    stop = 1
    run = 2


# Custom class to allow for custom points
class DeliveryPoint:
    def __init__(self, jointsDegree, name):
        self.jointsDegree = jointsDegree
        self.name = name


# Custom class to allow for custom points
class PickupPoint:
    def __init__(self, jointsDegree, name):
        self.jointsDegree = jointsDegree
        self.name = name


# Purpose: Converting from degrees to radians
# Input(Type = float / list[float]): angle (In degrees)
# Output(Type = float / list[float]): angle (In radians)
def degreeToRads(angle):
    # FORMULA USED TO CONVERT FROM DEGREE TO RADS
    #  Angle in radians = Angle in degrees * (π/180)
    #  0.01745 comes from this quotient (π/180)
    if isinstance(angle, list):
        jointsAngleRads = []
        for joint in angle:
            jointsAngleRads.append(round(float(joint) * 0.01745), 2)
        return jointsAngleRads
    else:
        return round(angle * 0.01745, 2)


# Purpose: Converting from radians to degrees
# Input(Type = float / list[float]): angle (In radians)
# Output(Type = float / list[float]): angle (In degrees)
def radsToDegree(angle):
    # FORMULA USED TO CONVERT FROM RADS TO DEGREE
    #  Angle in degrees = Angle in radians * (180/π)
    #  57.29578 comes from this quotient (180/π)
    if isinstance(angle, list):
        jointsAngleDegree = []
        for joint in angle:
            jointsAngleDegree.append(round(float(joint) * 57.29578), 2)
        return jointsAngleDegree
    else:
        return round(angle * 57.29578, 2)


def arrDegreeToRads():
    jointNames = ["Base", "Shoulder", "Elbow", "Wrist 1", "Wrist 2", "Wrist 3"]
    jointsAngleRads = []
    for joints in jointNames:
        print("Give %s Angle in Degrees:" % joints)
        jointsAngleRads.append(float(input()) * 0.017453)
    print("This is the angles in rads")
    count = 0
    arrayLength = len(jointsAngleRads)
    for x in jointsAngleRads:
        if (count == 0):
            print("[", end='')
        if (count == arrayLength - 1):
            print("{:.2f}".format(x), end='')
        else:
            print("{:.2f}".format(x), end=',')
        count += 1
    print("]")


def printMenu():
    print("1) Start Program")
    print("2) something ")
    print("3) something")
    print("4) Add Faces/Orders")
    print("5) Add Pick/Delivery Zones")
    print("0) Exit")


def setNewPickUp(arm):
    print("You are about to enter free drive mode.")
    print("In this mode the arm will unlock and allow you to")
    print("psychically move the arm to the desired position.")
    print("After entering 'go' the arm will unlock and at that")
    print("time move the arm to the desired position. When done moving")
    print("press the enter key to lock the arm and save the position.")
    print("The free drive mode will timeout at 60 seconds if not ended.")
    print("")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("THE ARM MAY NOT BE ABLE TO SUPPORT ITS OWN WEIGHT HAVE")
    print("ONE HAND ON THE ARM WHEN YOU START FREE DRIVE MODE")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("")
    while True:
        print("Enter 'go' to start free drive mode.", end=':')
        userChoice = input().lower()
        if userChoice != "go":
            break
        else:
            print("%s is not a valid option", userChoice)
            print("")

    arm.set_freedrive(True)
    # This should start some timer that will end if the user presses enter however if they don't it will end the loop
    print("The arm is in free drive mode, you can move it now.")
    print("")
    print("Press the enter key to lock the arm and save the position", end=':')

    if input() == "":
        arm.set_freedrive(False)

    return arm.getj()
    # This might need to be converted if so the function degreeToRads( variable ) should work




def main():
    programState = Modes.stop

    mainDeliveryPoint = DeliveryPoint([0, 1.57, -1.57, 3.14, -1.57, 1.57], "Main")
    mainPickupPoint = PickupPoint([0, 1.57, -1.57, 3.14, -1.57, 1.57], "Main")

    deliveryPointList = [mainDeliveryPoint]
    pickupPointList = [mainPickupPoint]

    robotArm = urx.Robot("localhost")
    # The below set up is a random/default for the TCP and payload. Details on the numbers to put in is in the link below
    # https://academy.universal-robots.com/modules/e-Series%20core%20track/English/module3/story_html5.html?courseId=2166&language=English
    robotArm.set_tcp((0, 0, 0.1, 0, 0, 0))
    robotArm.set_payload(2, (0, 0, 0.1))
    time.sleep(0.2)  # leave some time to robot to process the setup commands
    print("Starting Main Loop")
    while True:
        printMenu()
        print(":")
        userChoice = int(input())
        if userChoice == 1:  # Start Program
            programState = Modes.run
        elif userChoice == 2:  # something
            programState = Modes.stop
        elif userChoice == 3:  # something
            programState = Modes.stop
        elif userChoice == 4:  # Add Faces/Orders
            programState = Modes.stop
        elif userChoice == 5:  # Add Pick/Delivery Zones
            # Need to add a thing to ask if they want to add a pick up or delivery point
            # The data also need to be validated and i should make it so that people can enter their own joint values
            # I already made the function for this  ^
            deliveryPointList.append(setNewPickUp(robotArm))
            programState = Modes.stop
        elif userChoice == 0:  # Exit
            programState = Modes.stop
        print(programState)

        while programState == Modes.run:
            print(robotArm.get_pos())
            time.sleep(0.1)

            # if found face that has delivery
            #   tell arm to go to pickup the spot
            #   tell arm to grab
            #   tell arm to go to delivery spot
            #   tell arm to drop
            #   tell arm to go to wait stop


if __name__ == '__main__':
    main()
