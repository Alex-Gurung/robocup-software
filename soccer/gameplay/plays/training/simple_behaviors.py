import robocup
import constants
import play
import skills
import tactics

# This is a file where you can learn how skills work!
class SimpleBehaviors(play.Play):

    def __init__(self):
        super().__init__(continuous=True)

        # To make a robot move, use skills.move.Move(<point to move to>)
        # To create a point, we initialize a point using 
        # robocup.Point(<x coordinate>, <y coordinate>)
        
        # These lines moves a robot to the point (0, 0)
        field_length = constants.Field.Length
        field_width = constants.Field.Width / 2
        
        capture_skill = skills.capture.Capture()

        line_kick_skill = skills.line_kick.LineKick()
        
        pivot_kick_skill = skills.pivot_kick.PivotKick()
        
        self.add_subbehavior(capture_skill, "capture")
        self.add_subbehavior(line_kick_skill, "linekick")   
        self.add_subbehavior(pivot_kick_skill, "pivotkick")

        # move_point = robocup.Point(field_width, 0)
        # skill = skills.move.Move(move_point)
        
        # # Adds behavior to our behavior tree, we will explain this more later
        # self.add_subbehavior(skill, "skill")
        
        # move_point = robocup.Point(field_width, field_length)
        # skill = skills.move.Move(move_point)

        # self.add_subbehavior(skill, "skill2")
        
        # move_point = robocup.Point(-field_width, 0)
        # skill = skills.move.Move(move_point)
        # self.add_subbehavior(skill, "skill3")
        
        # move_point = robocup.Point(-field_width, field_length)
        # skill = skills.move.Move(move_point)
        # self.add_subbehavior(skill, "skill4")
        