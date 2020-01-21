from moviepy.editor import *

def convertToGif(filenamee, newname):
    
    castle = (VideoFileClip(filenamee, audio=False)
              .subclip(22.8,23.2)
              .speedx(1.5)
              .resize(2))

    d = castle.duration
    castle = castle.crossfadein(d/2)

    composition = (CompositeVideoClip([castle,
                                       castle.set_start(d/2),
                                       castle.set_start(d)])
                   .subclip(d/2, 3*d/2))

    composition.write_gif(newname, fps=5,fuzz=5)

