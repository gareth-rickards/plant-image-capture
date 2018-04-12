from unrealcv import client


class Map(object):

    def __init__(self):
        pass

    def get_view_mode(self):
        return client.request('vget /viewmode')

    def set_view_mode(self, view_mode):
        client.request('vset /viewmode %s' % view_mode)
        if view_mode == 'object_mask':
            # Change floor colour
            client.request('vset /object/Floor/color 136 109 92')

    def capture(self, view_mode, camera, plant, camera_position):
        # Remove all plants except the one we want to capture from map
        client.request('vset /object/%s/location 0 15 20' % plant.name)
        for degree in range(0, 360, 80):
            camera.take_picture(plant.name, view_mode, degree, camera_position)
            degree += 1
            print "Rotating plant..."
            plant.rotate('0 %d 0' % degree)
            # client.request('vset /object/%s/rotation 0 %d 0' % (plant, degree))
        print "Moving weed out of view..."
        plant.move('40 0 200')
        # client.request('vset /object/%s/location 40 0 200' % plant)


class Camera(object):

    def __init__(self):
        pass

    def take_picture(self, plant, view_mode, degree, camera_position):
        # Take a picture of the plant
        print "Taking %s %s picture %d from %s" % (plant, view_mode, degree, camera_position)
        image = client.request('vget /camera/0/%s png' % view_mode)
        with open('D:\sudo_hackathon_pics\%s_%s_%s_%d.png' % (plant, view_mode, camera_position, degree), 'wb') as f:
            f.write(image)

    def move(self, location):
        client.request('vset /camera/0/location %s' % location)

    def rotate(self, rotation):
        client.request('vset /camera/0/rotation %s' % rotation)


class Plant(object):

    def __init__(self, name):
        self.name = name

    def set_plant_colour(self, object, colour):
        client.request('vset /object/%s/color %s' % (object, colour))

    def move(self, location):
        client.request('vset /object/%s/location %s' % (self.name, location))

    def rotate(self, rotation):
        client.request('vset /object/%s/rotation %s' % (self.name, rotation))


if __name__ == '__main__':
    client.connect()  # Connect to the game
    if not client.isconnected():  # Check if the connection is successfully established
        print 'UnrealCV server is not running.'

    plants = []
    oat_camera_coordinates = {'Position': '', 'Rotation': ''}
    dandelion_camera_coordinates = {'Position': '', 'Rotation': ''}

    objects = client.request('vget /objects').split(' ')

    for item in objects:
        # Put the plant objects into the plants list.
        if item.startswith('dandelion') or item.startswith('oat'):
            plants.append(Plant(name=item))
    print('Number of weeds in this scene:', len(plants))

    camera = Camera()

    oat_camera_coordinates['Position'] = '0 0 45'
    oat_camera_coordinates['Rotation'] = '-50 90 0'

    dandelion_camera_coordinates['Position'] = '0 3 35'

    # Move all plants out of the camera's view
    for plant in plants:
        print client.request('vset /object/%s/location 40 0 200' % plant.name)

    game_map = Map()

    game_map.set_view_mode('lit')

    for plant in plants:
        camera.move(
            oat_camera_coordinates['Position'] if plant.name == 'oat' else dandelion_camera_coordinates['Position'])
        camera.rotate(oat_camera_coordinates['Rotation'])
        game_map.capture(game_map.get_view_mode(), camera, plant, 'angle')

    game_map.set_view_mode('object_mask')

    for plant in plants:
        game_map.capture(game_map.get_view_mode(), camera, plant, 'angle')


    # dandelion_camera_coordinates['Position'] = '0 3 35'
    # set_camera_position(dandelion_camera_coordinates['Position'])
    # capture(get_view_mode(), 'dandelion', 'angle')
    #
    # set_view_mode('object_mask')
    # set_camera_position(oat_camera_coordinates['Position'])
    # capture(get_view_mode(), 'oat', 'angle')
    # set_camera_position(dandelion_camera_coordinates['Position'])
    # set_object_colour('dandelion', '0 250 0')
    # capture(get_view_mode(), 'dandelion', 'angle')
    #
    # set_view_mode('lit')
    # oat_camera_coordinates['Position'] = '0 15 50'
    # oat_camera_coordinates['Rotation'] = '-100 0 0'
    # set_camera_position(oat_camera_coordinates['Position'], oat_camera_coordinates['Rotation'])
    # capture(get_view_mode(), 'oat', 'top')
    #
    # dandelion_camera_coordinates['Position'] = '0 15 40'
    # set_camera_position(dandelion_camera_coordinates['Position'])
    # capture(get_view_mode(), 'dandelion', 'top')
    #
    # set_view_mode('object_mask')
    # oat_camera_coordinates['Position'] = '0 15 50'
    # oat_camera_coordinates['Rotation'] = '-100 0 0'
    # set_camera_position(oat_camera_coordinates['Position'], oat_camera_coordinates['Rotation'])
    # capture(get_view_mode(), 'oat', 'top')
    #
    # dandelion_camera_coordinates['Position'] = '0 15 40'
    # set_camera_position(dandelion_camera_coordinates['Position'])
    # set_object_colour('dandelion', '0 250 0')
    # capture(get_view_mode(), 'dandelion', 'top')
