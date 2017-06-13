import math

class LineFollower:
    def __init__(self):
        self.KSI = 0.56
        self.W_N = 5
        self.V_RATIO = 50  # Is not calculated
        self.DISTANCE_BETWEEN_AXIS
        self.DISTANCE_BETWEEN_WHEELS
        

    def normalize(self, vector):
        n = len(vector)
        magnitude = 0
        for i in range(0, n, 1):
            magnitude += vector(i)**2
        magnitude = math.sqrt(magnitude)
        vector = vector/magnitude
        return vector

    def setControlData(self, car, desired_position, line_ref, velocity):

        if (desired_position.translation.x - car.x) * line_ref.x + (desired_position.translation.y - car.y) * line_ref.y < 0:
            line_ref = -line_ref

        line_ref = self.normalize(line_ref)

        rotation = car.rotation
        phiLine = math.atan2(line_ref.y, line_ref.x)# ref angle
        positionError = math.sqrt((car.x - desired_position.x) * (car.x - desired_position.x) + (car.y - desired_position.y) * (car.y - desired_position.y))
        lineError = car.x * line_ref.y - car.y * line_ref.x + line_ref.x * desired_position.y - line_ref.y * desired_position.x
        phiError = phiLine - rotation






# void LineControl::setControlData(representations::Player &player, modeling::WorldModel &wm,
#                                     Pose2D desiredPosition, Vector2<double> lineRef, double velocity) {
#     if ((desiredPosition.translation.x - player.getPose().translation.x) * lineRef.x +
#         (desiredPosition.translation.y - player.getPose().translation.y) * lineRef.y < 0)
#         lineRef = -lineRef;
#
#     lineRef = normalize(lineRef)
#
#     //double angularVelocity = player.getAngularVelocity();
#     //double robotVelocity = player.getVelocity();
#     double maxVelocity = velocity; // Max velocity reference
#     double rotation = player.getRotation();  //player angle
#     double phiLine = atan2(lineRef.y, lineRef.x);  //ref angle
#     double radius = representations::Player::WHEEL_RADIUS;
#     double distanceWheels = representations::Player::DISTANCE_WHEELS;
#     double wr = 0;
#     double wl = 0;
#     double vratio = V_RATIO;
#     double positionError = sqrt(
#             (player.getPose().translation.x - desiredPosition.translation.x) *
#             (player.getPose().translation.x - desiredPosition.translation.x)
#             + (player.getPose().translation.y - desiredPosition.translation.y) *
#               (player.getPose().translation.y - desiredPosition.translation.y));
#     double lineError = player.getPosition().x * lineRef.y - player.getPosition().y * lineRef.x
#                        + lineRef.x * desiredPosition.translation.y - lineRef.y * desiredPosition.translation.x;
#     double K_PHI = 2 * KSI * W_N;
#     double K_H = W_N / (2 * KSI * maxVelocity);
#     //Saturation
#
#     //Angular error
#     double phiErro = phiLine - rotation;
#
#
#     //Anti wind up
#
#     if (positionError < 0.04) {
#         desiredWheelSpeed.left = 0.0;
#         desiredWheelSpeed.right = 0.0;
#         return;
#     }
#
#     if (rotation > M_PI / 3)
#         rotation = M_PI / 3;
#     if (rotation < -M_PI / 3)
#         rotation = -M_PI / 3;
#     //Change of state
#
#     //Velocity control
#
#     //Do control
#
#     //Integrative
#     if (positionError < 0.15) {
#         maxVelocity = 10;
#         K_H = W_N / (2 * KSI * fabs(maxVelocity));
#     }
#     if (phiErro > M_PI)
#         phiErro -= 2 * M_PI;
#     if (phiErro < -M_PI)
#         phiErro += 2 * M_PI;
#     if (phiErro < -M_PI / 2) {
#         phiErro += M_PI;
#         maxVelocity = -maxVelocity;
#         vratio = -vratio;
#     }
#     if (phiErro > M_PI / 2) {
#         phiErro -= M_PI;
#         maxVelocity = -maxVelocity;
#         vratio = -vratio;
#     }
#     // controle da velocidade  da roda direita
#     wr = maxVelocity + distanceWheels * (K_PHI * (K_H * lineError + phiErro)) / (2 * radius);
#     // controle da velocidade da roda esquerda
#     wl = maxVelocity - distanceWheels * (K_PHI * (K_H * lineError + phiErro)) / (2 * radius);
#     //Stop condition
#
#     //TODO: Change constants instead of multiplying by (M_PI/30);
#     desiredWheelSpeed.left = wl;
#     desiredWheelSpeed.right = wr;
#
# }
#
# }
# }
