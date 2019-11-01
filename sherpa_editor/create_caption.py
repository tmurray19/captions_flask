
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os, logging, time, datetime
from app import app
from flask import url_for


sizes = {
    "Small": 12,
    "Medium": 20,
    "Large": 80,
    "X-Large": 160,
    "XX-Large": 400
}


def generate_caption(pos, proj_id, vid_id, capt, colour, font, font_size):
    pos = [int(p) for p in pos]
    print(pos)
    vid = VideoFileClip(
        os.path.join(
            app.config['BASE_DIR'], 
            app.config['VIDS_LOCATION'], 
            str(proj_id), 
            str(vid_id)+".mp4"
        )
    )
    vid = vid.subclip(0, vid.duration).resize((852, 480))

    print(int(sizes[font_size] * 0.44357))
    caption = TextClip(
        txt=capt,
        fontsize=int(sizes[font_size] * 0.44357),
        color='#' + str(colour),
        font=font
    ).set_position(pos).set_duration(vid.duration)

    vid = CompositeVideoClip([vid, caption])

    ts=time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')

    vid.save_frame(
        os.getcwd() + '/app/static/img/' + str(proj_id) + '/{}_frame_caption_{}.png'.format(str(vid_id), st)
    )


    return '/static/img/{}/{}_frame_caption_{}.png'.format(str(proj_id), str(vid_id), st)

