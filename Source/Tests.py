################################################################################
# Imports
################################################################################

from unittest import TestCase
from Main import *



class TestGenerate_maze_depth_first_search(TestCase):
	def test_generate_maze_depth_first_search(self):
		self.fail()


class TestGet_open_tile_coordinates(TestCase):
	def test_get_open_tile_coordinates(self):
		self.fail()


class TestDraw_maze(TestCase):
	def test_draw_maze(self):
		self.fail()


class TestGet_cell_rect(TestCase):
	def test_get_cell_rect(self):
		self.fail()


class TestDraw_door_object(TestCase):
	def test_draw_door_object(self):
		self.fail()


class TestDraw_chest_object(TestCase):
	def test_draw_chest_object(self):
		self.fail()


class TestDraw_key_object(TestCase):
	def test_draw_key_object(self):
		self.fail()


class TestDraw_player_object(TestCase):
	def test_draw_player_object(self):
		self.fail()


class TestPosition_is_occupied(TestCase):
	def test_position_is_occupied(self):
		from Main import position_is_occupied
		self.assertTrue(position_is_occupied(0, 0))
		self.assertTrue(position_is_occupied(0, 1))
		self.assertTrue(position_is_occupied(1, 0))
		self.assertTrue(position_is_occupied(1, 1))


class TestGo(TestCase):
	def test_go(self):
		from Main import go
		self.assertIsNone(go(0, 0))
		self.assertIsNone(go(0, 1))
		self.assertIsNone(go(1, 0))
		self.assertIsNone(go(1, 1))


class TestPlayer_next_to_object(TestCase):
	def test_player_next_to_object(self):
		from Main import player_next_to_object
		self.assertTrue(player_next_to_object(0, 0, 0, 0))
		self.assertTrue(player_next_to_object(0, 0, 0, 1))
		self.assertTrue(player_next_to_object(3, 2, 2, 1))
		self.assertTrue(player_next_to_object(4, 2, 3, 2))
		self.assertTrue(player_next_to_object(3, 2, 4, 2))
		self.assertTrue(player_next_to_object(3, 2, 2, 3))
		self.assertTrue(player_next_to_object(21, 15, 21, 16))
		self.assertTrue(player_next_to_object(12, 35, 13, 36))
		self.assertFalse(player_next_to_object(53, 2, 28, 19))
		self.assertFalse(player_next_to_object(100, 4222, 40, 6))


class TestOpen_door(TestCase):
	def test_open_door(self):
		player_object_position[0] = 3
		player_object_position[1] = 2
		door_object_position[0] = 2
		door_object_position[1] = 1
		self.assertIsNone(open_door())
		if player_next_to_object(3, 2, 2, 1):
			if player_used_key is True and player_opened_chest is True:
					self.assertTrue(open_door())
			if not player_used_key and not player_opened_chest:
				self.assertFalse(open_door())

'''
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
'''