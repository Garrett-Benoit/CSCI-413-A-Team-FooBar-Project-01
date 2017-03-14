from unittest import TestCase
from Main import *

class TestPlayer_grabKey(TestCase)
	def test_player_grab_key(self):
	
		player_object_position[0] = 5
		player_object_position[1] = 14
		key_object_position[0] = 6
		key_object_position[1] = 14


		self.assertTrue(player_next_to_door(5, 14, 6, 14))
		self.assertFalse(player_next_to_door(18, 4, 20, 10))

class TestPlayer_openChest(TestCase)
	def test_player_open_chest(self):
		self.assertTrue(player_next_to_object(1, 2, 2, 3))
		self.assertTrue(player_next_to_object(5, 8, 4, 8))
		self.assertTrue(player_next_to_object(12, 3, 12, 2))
		self.assertTrue(player_next_to_object(18, 20, 19, 20))
		self.assertFalse(player_next_to_object(5, 7, 20, 12))
	


class TestPlayer_openDoor(TestCase)
	def test_player_open_door(self):
		from Main import open_door
	
		player_object_position[0] = 4
		player_object_position[1] = 3
		door_object_position[0] = 3
		door_object_position[1] = 3

		if player_next_to_object(4, 3, 3, 3):
			if player_used_key is True and player_opened_chest is True:
				self.assertTrue(open_door())
			if player_used_key is False and player_opened_chest is False:
				self.assertFalse(open_door())