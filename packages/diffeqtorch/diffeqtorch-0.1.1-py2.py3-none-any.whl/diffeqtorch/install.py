import os
import subprocess
from pathlib import Path
from warnings import warn

from .logging import get_logger

JULIA_PROJECT = str(Path(__file__).parents[1])

log = get_logger("diffeqtorch_install")


def install_and_test(pyjulia=True, julia_deps=True, julia_sysimage=True):
    if pyjulia:
        install_pyjulia()
        test_pyjulia()

    if julia_deps:
        install_julia_deps()
        test_julia_deps()

    if julia_sysimage:
        install_julia_sysimage()
        test_julia_sysimage()


def install_julia_deps():
    log.debug("Install Julia dependencies")
    output = subprocess.run(
        f"export JULIA_PROJECT={JULIA_PROJECT}; julia -E 'using Pkg; Pkg.instantiate()'",
        shell=True,
        check=True,
        capture_output=True,
    )
    log.debug(output)


def test_julia_deps():
    output = subprocess.run(
        f"export JULIA_PROJECT={JULIA_PROJECT}; julia -E 'using DifferentialEquations'",
        shell=True,
        check=True,
        capture_output=True,
    )
    log.debug(output)


def install_pyjulia():
    log.debug("Install PyJulia")

    import julia

    julia.install()


def test_pyjulia(sysimage=None, call="1+1"):
    from julia.api import Julia

    if sysimage is None:
        julia = Julia(compiled_modules=False, debug=True)
    else:
        julia = Julia(compiled_modules=False, sysimage=sysimage, debug=True)

    log.debug(julia._call(call))


def install_julia_sysimage():
    if "JULIA_SYSIMAGE_DIFFEQTORCH" in os.environ:
        if not Path(os.environ["JULIA_SYSIMAGE_DIFFEQTORCH"]).exists():
            log.debug("Build Julia system image")
            output = subprocess.run(
                f"export JULIA_PROJECT={JULIA_PROJECT}; julia {JULIA_PROJECT}/sysimage.jl",
                shell=True,
                check=True,
                capture_output=True,
            )
            log.debug(output)
        else:
            log.debug("System image exists, skipping")
    else:
        warn("JULIA_SYSIMAGE_DIFFEQTORCH not set, won't build system image")


def test_julia_sysimage():
    if "JULIA_SYSIMAGE_DIFFEQTORCH" in os.environ:
        assert Path(os.environ["JULIA_SYSIMAGE_DIFFEQTORCH"]).exists()
        test_pyjulia(
            sysimage=os.environ["JULIA_SYSIMAGE_DIFFEQTORCH"],
            call="using DifferentialEquations",
        )
    else:
        log.debug("JULIA_SYSIMAGE_DIFFEQTORCH not set")
