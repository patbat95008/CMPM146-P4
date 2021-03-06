
import random

# EXAMPLE STATE MACHINE
class MantisBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None
    

  def handle_event(self, message, details):

    if self.state is 'idle':

      if message == 'timer':
        # go to a random point, wake up sometime in the next 10 seconds
        world = self.body.world
        x, y = random.random()*world.width, random.random()*world.height
        self.body.go_to((x,y))
        self.body.set_alarm(random.random()*10)

      elif message == 'collide' and details['what'] == 'Slug':
        # a slug bumped into us; get curious
        self.state = 'curious'
        self.body.set_alarm(1) # think about this for a sec
        self.body.stop()
        self.target = details['who']

    elif self.state == 'curious':

      if message == 'timer':
        # chase down that slug who bumped into us
        if self.target:
          if random.random() < 0.5:
            self.body.stop()
            self.state = 'idle'
          else:
            self.body.follow(self.target)
          self.body.set_alarm(1)
      elif message == 'collide' and details['what'] == 'Slug':
        # we meet again!
        slug = details['who']
        slug.amount -= 0.01 # take a tiny little bite
   
class SlugBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.have_resource = False


  def handle_event(self, message, details):
    # TODO: IMPLEMENT THIS METHOD
    #  (Use helper methods and classes to keep your code organized where
    #  approprioate.)
    print '!!!Message: ' + repr(message) + ' Details: ' + repr(details) + ' State: ' + repr(self.state)
    #listens for events to change state
    
    if isinstance(details, tuple):
       self.state = 'moving' 
       destination = details
    elif self.body.amount < 0.5:
       self.state = 'flee'    
    elif details == 'i':
       self.state = 'idle'
    elif details == 'a':
       self.state = 'attack'
    elif details == 'b':
       self.state = 'build'
    elif details == 'h':
       self.state = "harvest"
       
    
    #actions to do in each state
    #if self.state is 'idle':
    if self.state is 'idle':
      self.body.stop()
    #elif self.state is 'moving':
    elif isinstance(details, tuple):
       self.body.go_to(destination)
    elif self.state is 'attack':
    #elif details == 'a':
       self.body.set_alarm(2)
       enemy = self.body.find_nearest('Mantis')
       self.body.follow(enemy)
    elif self.state is 'build':   
    #elif details == 'b':
       self.body.set_alarm(5)
       nest = self.body.find_nearest('Nest')
       self.body.go_to(nest)
    elif self.state is 'harvest':
       if self.have_resource == False:
          res = self.body.find_nearest('Resource')
          self.body.go_to(res)
       else:
          nest = self.body.find_nearest('Nest')
          self.body.go_to(nest)
    elif self.state is 'flee':
       nest = self.body.find_nearest('Nest')
       self.body.go_to(nest)
       
       
    #if you're in attack mode, fight back!   
    if message == 'collide' and details['what'] == 'Mantis' and self.state == 'attack':
       unit = details['who']
       unit.amount -= 0.05
       
    #if you're in build mode, build nests
    if message == 'collide' and details['what'] == 'Nest' and self.state == 'build':
       unit = details['who']
       unit.amount += 0.01
       
    #if you're in harvest mode, harvest 
    if message == 'collide' and details['what'] == 'Nest' and self.state == 'harvest':
       self.have_resource = False
       
    if message == 'collide' and details['what'] == 'Resource' and self.state == 'harvest' and self.have_resource == False:
       self.have_resource = True
       unit = details['who']
       unit.amount -= 0.25
    
    if message == 'collide' and details['what'] == 'Nest' and self.state == 'flee':
       self.body.amount = 1
    
    #debugger message; gets commands and details for understanding
    #if message is not 'collide':
    #print '!!!Message: ' + repr(message) + ' Details: ' + repr(details) + ' State: ' + repr(self.state)

world_specification = {
  'worldgen_seed': 13, # comment-out to randomize
  'nests': 2,
  'obstacles': 25,
  'resources': 5,
  'slugs': 5,
  'mantises': 5,
}

brain_classes = {
  'mantis': MantisBrain,
  'slug': SlugBrain,
}
