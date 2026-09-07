import pywinctl as pwc
import pymonctl as pmc

window = pwc.getActiveWindow()
print("Window's Active Display:", window.getDisplay())

print("Window Box Model:", window.box)

print("Window Extra Frame Size:", window.getExtraFrameSize())
print("Window Client Frame:", window.getClientFrame())

# Monitor Stuff
# monitors: list[pmc.Monitor] = pmc.getAllMonitors()
#
# for monitor in monitors:
#     print(monitor.name)
#
# monitor = pmc.getAllMonitors()[1]

# print(monitor.size)
# print(monitor.position)

# Docking to the left half of second monitor
# window.restore()
# window.moveTo(monitor.position.x - 16, monitor.position.y)
# window.resizeTo(monitor.size.width // 2 + 16, monitor.size.height)