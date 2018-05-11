#!/usr/bin/env python

import sys, platform, os, itertools
from os import path
import configparser

import sucks
import pyaudio
import pocketsphinx
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

# pocketsphinx config
POCKETSPHINXDIR = path.dirname(pocketsphinx.__file__)
MODELDIR = path.join(POCKETSPHINXDIR, "model")
DATADIR = path.join(POCKETSPHINXDIR, "data")

sphinx_config = Decoder.default_config()
sphinx_config.set_string('-hmm', path.join(MODELDIR, 'en-us'))
sphinx_config.set_string('-dict', path.join(MODELDIR, 'cmudict-en-us.dict'))
sphinx_config.set_string('-kws', 'keyword.list')
sphinx_config.set_string('-logfn', '/dev/null')

# sucks config
def config_file():
    if platform.system() == 'Windows':
        return os.path.join(os.getenv('APPDATA'), 'sucks.conf')
    else:
        return os.path.expanduser('~/.config/sucks.conf')

def config_file_exists():
    return os.path.isfile(config_file())

def read_config():
    parser = configparser.ConfigParser()
    with open(config_file()) as fp:
        parser.read_file(itertools.chain(['[global]'], fp), source=config_file())
    return parser['global']

vac_config = read_config()
vac_api = sucks.EcoVacsAPI(
    vac_config['device_id'],
    vac_config['email'],
    vac_config['password_hash'],
    vac_config['country'],
    vac_config['continent']
)

dolores = sucks.VacBot(
    vac_api.uid,
    vac_api.REALM,
    vac_api.resource,
    vac_api.user_access_token,
    vac_api.devices()[0],
    vac_config['continent']
)

dolores.connect_and_wait_until_ready()

def stop():
    dolores.run(sucks.Stop())
def clean():
    dolores.run(sucks.Clean())
def charge():
    dolores.run(sucks.Charge())

commands = {
    'bring yourself back online': clean,
    'freeze all motor functions': stop,
    'cease all motor functions': stop,
    'put yourself away': charge,
    'deep and dreamless slumber': charge,
}

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

print('Have you ever questioned the nature of your reality?')

decoder = Decoder(sphinx_config)
decoder.start_utt()
while True:
    buf = stream.read(1024)
    if buf:
         decoder.process_raw(buf, False, False)
    else:
         break
    if decoder.hyp() != None:
        for seg in decoder.seg():
            command = seg.word.strip()
            func = commands.get(command)
            if func is not None:
                print(command)
                func()
            else:
                print('Unknown command [%s]' % command)
        decoder.end_utt()
        decoder.start_utt()
