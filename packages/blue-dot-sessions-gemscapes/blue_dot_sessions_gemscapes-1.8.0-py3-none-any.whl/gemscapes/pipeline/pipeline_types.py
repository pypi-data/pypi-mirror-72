import typing

__all__ = [
    "PipelineFnReturnType",
    "PipelineFnType",
    "ComputeStatsPipelineFnType",
    "ComputeStatsPipelineEndFnType"
]


PipelineFnReturnType = typing.Tuple[str, typing.Dict[str, typing.Any]]
PipelineFnType = typing.Callable[[str, typing.Optional[bool]], PipelineFnReturnType]

ComputeStatsPipelineFnType = typing.Callable[[str], str]
ComputeStatsPipelineEndFnType = typing.Callable[[str], typing.Dict[str, float]]
