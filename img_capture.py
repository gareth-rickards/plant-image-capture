from unrealcv import client


def take_picture(weed, view_mode, degree, camera_position):
    # Take a picture of the weed
    print "Taking %s %s picture %d from %s" % (weed, view_mode, degree, camera_position)
    image = client.request('vget /camera/0/%s png' % view_mode)
    with open('D:\sudo_hackathon_pics\%s_%s_%s_%d.png' % (weed, view_mode, camera_position, degree), 'wb') as f:
        f.write(image)


def set_view_mode(view_mode):
    client.request('vset /viewmode %s' % view_mode)
    if view_mode == 'object_mask':
        client.request('vset /object/Floor/color 139 69 19')


def get_view_mode():
    return client.request('vget /viewmode')


def set_camera_position(position='', rotation=''):
    if position:
        client.request('vset /camera/0/location %s' % position)
    if rotation:
        client.request('vset /camera/0/rotation %s' % rotation)


def capture(view_mode, plant, camera_position):
    # Remove all weeds except current_weed from map
    client.request('vset /object/%s/location 0 15 20' % plant)
    for degree in range(0, 360, 1):
        take_picture(plant, view_mode, degree, camera_position)
        degree += 1
        print "Rotating plant..."
        client.request('vset /object/%s/rotation 0 %d 0' % (plant, degree))
    print "Moving weed out of view..."
    client.request('vset /object/%s/location 40 0 200' % plant)


if __name__ == '__main__':
    client.connect()  # Connect to the game
    if not client.isconnected():  # Check if the connection is successfully established
        print 'UnrealCV server is not running. Run the game from http://unrealcv.github.io first.'

    weeds = []
    oat_camera_coordinates = {'Position': '', 'Rotation': ''}
    dandelion_camera_coordinates = {'Position': '', 'Rotation': ''}
    objects = client.request('vget /objects').split(' ')
    for item in objects:
        if item.startswith('dandelion') or item.startswith('oat'):
            weeds.append(item)
    print('Number of weeds in this scene:', len(weeds))

    # Rotate the camera to point to where the weeds will be
    oat_camera_coordinates['Position'] = '0 0 45'
    oat_camera_coordinates['Rotation'] = '-50 90 0'
    set_camera_position(oat_camera_coordinates['Position'], oat_camera_coordinates['Rotation'])
    # Move all plants out of the camera's view
    for plant in weeds:
        print client.request('vset /object/%s/location 40 0 200' % plant)

    set_view_mode('lit')
    capture(get_view_mode(), 'oat', 'angle')

    dandelion_camera_coordinates['Position'] = '0 3 35'
    set_camera_position(dandelion_camera_coordinates['Position'])
    capture(get_view_mode(), 'dandelion', 'angle')

    set_view_mode('object_mask')
    set_camera_position(oat_camera_coordinates['Position'])
    capture(get_view_mode(), 'oat', 'angle')
    set_camera_position(dandelion_camera_coordinates['Position'])
    capture(get_view_mode(), 'dandelion', 'angle')

    set_view_mode('lit')
    oat_camera_coordinates['Position'] = '0 15 50'
    oat_camera_coordinates['Rotation'] = '-100 0 0'
    set_camera_position(oat_camera_coordinates['Position'], oat_camera_coordinates['Rotation'])
    capture(get_view_mode(), 'oat', 'top')

    dandelion_camera_coordinates['Position'] = '0 15 40'
    set_camera_position(dandelion_camera_coordinates['Position'])
    capture(get_view_mode(), 'dandelion', 'top')

    set_view_mode('object_mask')
    oat_camera_coordinates['Position'] = '0 15 50'
    oat_camera_coordinates['Rotation'] = '-100 0 0'
    set_camera_position(oat_camera_coordinates['Position'], oat_camera_coordinates['Rotation'])
    capture(get_view_mode(), 'oat', 'top')

    dandelion_camera_coordinates['Position'] = '0 15 40'
    set_camera_position(dandelion_camera_coordinates['Position'])
    capture(get_view_mode(), 'dandelion', 'top')
