import robocup
import constants
import play
import skills
import tactics

class MoveToCorner(play.Play):
    def __init__(self):
        
        width = constants.Field.Width
        corner = robocup.Point(width / 2, 0)
        skill = skills.move.Move(corner)
        self.add_subbehavior(skill, "CornerMove")