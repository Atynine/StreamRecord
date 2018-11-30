import argparse
import os
import streamlink
from streamlink import Streamlink


class Record:
    session = Streamlink()
    stream_url = ""
    quality = ""
    output = ""
    block_size = 0
    max_blocks = 0
    debug = False

    def __init__(self, stream_url, quality):
        self.stream_url = stream_url
        self.quality = quality

    def record(self):
        print("Checking for stream to record from {}".format(self.stream_url))
        streams = self.session.streams(self.stream_url)
        if len(streams) == 0:
            print("\nUnable to load stream. The stream may be offline.")
            return 0
        if self.quality not in streams:
            print("\nUnable to load quality {}. Available quality options are:".format(self.quality))
            for q in streams:
                print(q)
            return 0
        stream = streams[self.quality]

        print("Found stream for {} with {} quality.".format(self.stream_url, self.quality))
        try:
            reader = stream.open()
        except streamlink.StreamError as e:
            print("Error opening stream. {}".format(e))
            return 0
        print("Recording stream to " + self.output)

        # Create path if it doesn't exist
        if not os.path.exists(os.path.dirname(self.output)):
            print("Created directory {}".format(os.path.dirname(self.output)))
            os.makedirs(os.path.dirname(self.output))

        # Save stream to file
        file = open(self.output, "ab")
        if self.max_blocks <= 0:
            i = 0
            while True:
                i += 1
                data = reader.read(self.block_size)
                file.write(data)
                if self.debug != 0:
                    if self.max_blocks <= 0:
                        print("Saved {} blocks".format(i))
                    else:
                        print("Saved {} blocks of {}".format(i, self.max_blocks))
        else:
            for i in range(0, self.max_blocks):
                data = reader.read(self.block_size)
                file.write(data)
                if self.debug != 0:
                    if self.max_blocks <= 0:
                        print("Saved {} blocks".format(i))
                    else:
                        print("Saved {} blocks of {}".format(i, self.max_blocks))
        file.close()
        return 1


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", help="URL of the stream to record", required=True)
    parser.add_argument("-o", help="Output path", type=str, required=True)
    parser.add_argument("-q", help="Quality to record at. Default:best", default="best")
    parser.add_argument("-b", help="Block size in bytes to read from stream. Default:1024", default=256, type=int)
    parser.add_argument("-n", help="Number of blocks to record. 0=Infinite. Default:0", default=0, type=int)
    parser.add_argument("-d", help="Debug(True/False) Default:False", default=False, type=bool)

    args = parser.parse_args()

    recorder = Record(args.s, args.q)
    recorder.block_size = args.b
    recorder.output = args.o
    recorder.debug = args.d
    recorder.max_blocks = args.n
    recorder.record()


if __name__ == "__main__":
    main()
