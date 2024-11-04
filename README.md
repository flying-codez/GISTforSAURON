# GISTforSAURON
This repository presents adaptation codes of the GIST pipeline to read SAURON IFS data cubes. It is part of the continuation of the B.R.A.V.E. project and focuses on kinematic analysis of SAURON-observed quiescent galaxies.

# Preface

This is not a guide to GIST even though it might include (in the ReadMe.pdf) helpful tips from challenges encountered along the way. It is highly recommended you read the [GIST Documentation](https://abittner.gitlab.io/thegistpipeline/) for its installation and operation and run the example before you tackle the adaptation of the pipeline. For more information about the B.R.A.V.E. research this was for, you can download the paper [here](https://etd.library.emory.edu/concern/etds/1j92g8682?locale=en).

# Disclaimers 

1. A more detailed README pdf file is available to guide you through the main points, tips, and structure. It was meant for anyone adding to the research with Dr. Batiste, hence some of the advice might not be directed at you but can still be generally applied.
2. This adaptation does not alter the internal pipeline, maintaining GIST's original flexibility and adaptability qualities. It simply readjusts the SAURON cube to match the desired GIST cube criteria and shape.
3. The project only used the kinematic analysis features of GIST, and hence has not been tested for the other IFS analysis data.
4. There is a proposed batch processing and imaging feature. The imaging feature was developed to obtain data within certain radii of the target galaxies, as this was one of the main scopes of the research.
