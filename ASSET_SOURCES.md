# Chapel reference and asset sources

## Location and photographs

The chapel is Igreja da Ordem Terceira de São Francisco da Penitência, Rio de Janeiro, Brazil.
The filming location is reported by [Guitarload](https://guitarload.com.br/noticia/polyphia-anuncia-novo-album-e-lanca-clipe-gravado-no-rio-de-janeiro-veja-power-in-the-blood/).
The target is the eight-second frame of [Polyphia's POWER IN THE BLOOD](https://www.youtube.com/watch?v=fDltPLFdkYI&t=8s).

The [museum's official chapel page](https://saofranciscodapenitencia.org.br/capela_dourada.php) and its [virtual tour](https://my.matterport.com/show/?m=aq9JKXW5RH2) supplied additional visual reference.
Twenty gallery photos were downloaded for local study, with exact source URLs recorded in `outputs/polyphia-room/references/museum-sources.json`.
They are not included in the repository or used as projected scene textures.
The museum identifies the altar subject as the vision of the six-winged Christ appearing to Saint Francis.
Its description also confirms four twisted columns arranged in staggered planes.

## Saint Francis scan

- Work: *Frans af Assisi*, unknown artist, inventory KAS1959, Statens Museum for Kunst.
- Source: [Wikimedia Commons file and license record](https://commons.wikimedia.org/wiki/File:Ubekendt,_Frans_af_Assisi,_KAS1959,_Statens_Museum_for_Kunst,_3D_model.stl).
- Asset: `assets/statues/francis-assisi-smk.stl`.
- License: Creative Commons CC0 1.0 Universal Public Domain Dedication.

This is a substitute sculpture from another collection, not a scan of the statue in Rio.
The reconstruction normalizes its scale and uses a continuous carved-wood finish.
The packaged scene shares one reduced mesh between five instances, while the original full-resolution STL remains available for rebuilding.

## Anatomical base mesh

- Asset: `assets/statues/makehuman-base.obj`.
- Source: [MakeHuman base mesh](https://github.com/makehumancommunity/makehuman/blob/master/makehuman/data/3dobjs/base.obj).
- Authors named in the file: Data Collection AB, Joel Palmius, Jonas Hauquier, 2020.
- License: CC0, explicitly declared in the file header and [MakeHuman's asset license](https://github.com/makehumancommunity/makehuman/blob/master/LICENSE.md).
- Full asset license: `assets/statues/MAKEHUMAN-LICENSE.txt`.

Only graphical assets are used, not MakeHuman application code.
The Christ sculpture applies a custom pose and adds modeled drapery, hair, six feathered wings, and a sunburst.
It is an interpretation of the museum reference rather than an exact scan.
The bundled CC0 `caucasian-male-young.target` and `universal-male-young-maxmuscle-minweight.target` are stored locally as `male-young.target` and `male-lean-muscle.target`.
Both come from MakeHuman's `makehuman/data/targets/macrodetails/` directory in the same repository.
The `makehuman-weights.mhw` asset comes from `makehuman/data/rigs/default_weights.mhw` and explicitly declares CC0 in its metadata.
The weights preserve the torso while posing the arms.

## Rebuilding

Open the original `scenes/gilded-chapel-reconstruction.blend` and run `scripts/refine_chapel_from_references.py` once.
Then run `scripts/finish_chapel_anatomy.py` and `scripts/finish_chapel_composition.py` once, in that order.
Finally run `scripts/package_refined_chapel.py` to share the scan geometry and finalize the cameras and materials.
The scripts write a separate refined project under `outputs/polyphia-room/`.
The final saved project includes all geometry and requires no network access to render.
