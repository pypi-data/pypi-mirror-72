# Toil Pindel

[![travis badge][travis_badge]][travis_base]
[![codecov badge][codecov_badge]][codecov_base]
[![code formatting][black_badge]][black_base]

A toil wrapper for cgp pindel.

## Usage

This package uses docker to manage its dependencies, there are 2 ways of using it:

1. Running the [container][docker_base] in single machine mode without [`--batchSystem`] support:

    ```bash
    # using docker
    docker run -it papaemmelab/toil_pindel --help

    # using singularity
    singularity run docker://papaemmelab/toil_pindel --help
    ```

1. Installing the python package from [pypi][pypi_base] and passing the container as a flag:

    ```bash
    # install package
    pip install toil_pindel

    # run with docker
    toil_pindel [TOIL-OPTIONS] [PIPELINE-OPTIONS]
        --docker papaemmelab/toil_pindel
        --volumes <local path> <container path>
        --batchSystem LSF

    # run with singularity
    toil_pindel [TOIL-OPTIONS] [PIPELINE-OPTIONS]
        --singularity docker://papaemmelab/toil_pindel
        --volumes <local path> <container path>
        --batchSystem LSF
    ```

See [docker2singularity] if you want to use a [singularity] image instead of using the `docker://` prefix.

## Contributing

Contributions are welcome, and they are greatly appreciated, check our [contributing guidelines](.github/CONTRIBUTING.md)!

## Credits

This package was created using [Cookiecutter] and the
[papaemmelab/cookiecutter-toil] project template.

<!-- References -->
[singularity]: http://singularity.lbl.gov/
[docker2singularity]: https://github.com/singularityware/docker2singularity
[cookiecutter]: https://github.com/audreyr/cookiecutter
[papaemmelab/cookiecutter-toil]: https://github.com/papaemmelab/cookiecutter-toil
[`--batchSystem`]: http://toil.readthedocs.io/en/latest/developingWorkflows/batchSystem.html?highlight=BatchSystem

<!-- Badges -->
[codecov_badge]: https://codecov.io/gh/papaemmelab/toil_pindel/branch/master/graph/badge.svg?token=gZkGuyXDdp
[codecov_base]: https://codecov.io/gh/papaemmelab/toil_pindel
[travis_badge]: https://travis-ci.com/papaemmelab/toil_pindel.svg?token=VymT5apURZYCYw4zJX7v&branch=master&status=passed
[travis_base]: https://travis-ci.com/papaemmelab/toil_pindel
[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black_base]: https://github.com/ambv/black

<!--
[![docker badge][docker_badge]][docker_base]
[![docker badge][automated_badge]][docker_base]
[![pypi badge][pypi_badge]][pypi_base]
[docker_base]: https://hub.docker.com/r/papaemmelab/toil_pindel
[docker_badge]: https://img.shields.io/docker/cloud/build/papaemmelab/toil_pindel.svg
[automated_badge]: https://img.shields.io/docker/cloud/automated/papaemmelab/toil_pindel.svg
[pypi_badge]: https://img.shields.io/pypi/v/toil_pindel.svg
[pypi_base]: https://pypi.python.org/pypi/toil_pindel
-->
