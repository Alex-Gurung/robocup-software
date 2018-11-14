import robocup
import play
import behavior
import skills.move
import skills.capture
import tactics.coordinated_pass
import constants
import main
import enum

class ShapePass(play.Play):
	class State(enum.Enum):
		#1 robot to get the ball
		setup = 1
		# 4 other ones passing
		passing = 4

	def __init__(self):
		super().__init__(continuous=True)
		self.add_state(ShapePass.State.setup,
                       behavior.Behavior.State.running)
		self.add_state(ShapePass.State.passing,
                       behavior.Behavior.State.running)

		self.add_transition(behavior.Behavior.State.start,
                            ShapePass.State.setup, lambda: True,
                            'immediately')
		self.add_transition(
            ShapePass.State.setup, ShapePass.State.passing, lambda: self.
            all_subbehaviors_completed(), 'all subbehaviors completed')

		self.shape_points = [
            robocup.Point(0, constants.Field.Length / 2.0 - constants.Robot.Radius * 3),
            robocup.Point(constants.Field.Width / 4,
                          constants.Field.Length / 4),
            robocup.Point(-constants.Field.Width / 4,
                          constants.Field.Length / 4),
            robocup.Point(-constants.Field.Width / 6,
            			  constants.Field.Length / 6),
            robocup.Point(constants.Field.Width / 6,
            			  constants.Field.Length / 6),      
        ]
	
	def on_enter_setup(self):
		print('Entering setup')
		closestPt = min(self.shape_points,
                        key=lambda pt: pt.dist_to(main.ball().pos))

		otherPts = list(self.shape_points)
		otherPts.remove(closestPt)

		for i in range(len(otherPts)):
			self.add_subbehavior(skills.move.Move(otherPts[i]), 'move' + str(i))
		self.add_subbehavior(skills.capture.Capture(), 'capture')

	def on_enter_passing(self):
		print('Entering passing')

	def execute_setup(self):
		print('Executing Setup')

	def execute_passing(self):
		print('Executing passing')
        # If we had a pass in progress before and it finished, remove it
		if self.has_subbehaviors():
			if self.all_subbehaviors()[0].is_done_running():
				self.remove_all_subbehaviors()

        # if we're not currently passing, start a new pass
		if not self.has_subbehaviors():
            # pick pass from and to points
			kickFrom = min(self.shape_points,
                           key=lambda pt: pt.dist_to(main.ball().pos))
			kickFromIdx = self.shape_points.index(kickFrom)
			kickToIdx = (kickFromIdx + 1) % len(self.shape_points)
			kickToPt = self.shape_points[kickToIdx]

            # add the pass subbehavior
			self.add_subbehavior(
                tactics.coordinated_pass.CoordinatedPass(kickToPt), 'pass')

	def on_exit_setup(self):
		print("Exiting setup")
		self.remove_all_subbehaviors()

	def on_exit_passing(self):
		print("Exiting passing")
		self.remove_all_subbehaviors()