import logging
from src.movement import RobotMovement

class NavigationSystem:
    def __init__(self):
        self.movement = RobotMovement()
        self.logger = logging.getLogger('Navigation')

    def avoid_obstacles(self, detected_objects):
        """
        Basic obstacle avoidance strategy
        """
        self.logger.info(f"Obstacle avoidance triggered for objects: {detected_objects}")
        
        # Simple avoidance logic
        if "person" in detected_objects or "obstacle" in detected_objects:
            self.logger.warning("Obstacle detected. Stopping and changing direction.")
            self.movement.stop()
            
            # Random direction change
            import random
            avoidance_actions = [
                self.movement.turn_left,
                self.movement.turn_right,
                self.movement.backward
            ]
            
            random.choice(avoidance_actions)()

    def map_environment(self):
        """
        Future implementation for environment mapping
        """
        self.logger.info("Environment mapping not yet implemented")
        pass
