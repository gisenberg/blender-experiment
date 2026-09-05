import json, tempfile, unittest
from pathlib import Path
from merge_render_frames import merge_frames

class MergeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        self.settings={'scene_sha256':'same-scene','frame_start':1,'frame_end':2}
    def tearDown(self):self.tmp.cleanup()
    def worker(self,name,frames,settings=None):
        p=self.root/name;(p/'pan-final-frames').mkdir(parents=True)
        (p/'render-settings.json').write_text(json.dumps(settings or self.settings))
        for frame,data in frames.items():(p/'pan-final-frames'/f'frame-{frame:04d}.png').write_bytes(data)
        return p
    def test_disjoint_workers_merge_and_resume(self):
        a=self.worker('a',{1:b'frame-one'});b=self.worker('b',{2:b'frame-two'});out=self.root/'merged'
        self.assertEqual(merge_frames([a,b],out)['frames'],2)
        self.assertEqual(merge_frames([a,b],out)['missing'],[])
    def test_mismatched_scene_rejected(self):
        a=self.worker('a',{1:b'a'});b=self.worker('b',{2:b'b'},dict(self.settings,scene_sha256='different'))
        with self.assertRaisesRegex(ValueError,'different scenes'):merge_frames([a,b],self.root/'out')
    def test_conflicting_frame_rejected(self):
        a=self.worker('a',{1:b'a'});b=self.worker('b',{1:b'different'})
        with self.assertRaisesRegex(ValueError,'Conflicting'):merge_frames([a,b],self.root/'out')
    def test_incomplete_collection_rejected(self):
        a=self.worker('a',{1:b'a'})
        with self.assertRaisesRegex(ValueError,'Missing 1 frames'):merge_frames([a],self.root/'out')

if __name__=='__main__':unittest.main()
