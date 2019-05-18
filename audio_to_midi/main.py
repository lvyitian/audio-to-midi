import argparse
import soundfile
import os
import numpy

from audio_to_midi import fft


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="The sound file to process.")
    parser.add_argument(
        "--output", "-o", help="The MIDI file to output. Default: <infile>.mid"
    )
    parser.add_argument(
        "--time-quantum",
        "-t",
        default=5.0,
        type=float,
        help="The time span over which to compute the individual FFTs in milliseconds.",
    )
    parser.add_argument(
        "--activation-level",
        "-a",
        default=0.0,
        type=float,
        help="The amplitude threshold for notes to be added to the MIDI file. Must be between 0 and 1.",
    )
    parser.add_argument(
        "--condense",
        "-c",
        action="store_true",
        help="Combine contiguous notes at their average amplitude.",
    )
    parser.add_argument(
        "--single-note",
        "-s",
        action="store_true",
        help="Only add the loudest note to the MIDI file for a given time span.",
    )
    args = parser.parse_args()

    args.output = (
        "{}.mid".format(os.path.basename(args.infile))
        if not args.output
        else args.output
    )

    samples, samplerate = soundfile.read(args.infile)

    if isinstance(samples[0], numpy.float64):
        samples = [[s] for s in samples]

    f = fft.FFT(
        samples=samples,
        channels=len(samples[0]),
        samplerate=samplerate,
        time_quantum=args.time_quantum,
        activation_level=args.activation_level,
        condense=args.condense,
        single_note=args.single_note,
        outfile=args.output,
    )
    f.calculate()


if __name__ == "__main__":
    main()
