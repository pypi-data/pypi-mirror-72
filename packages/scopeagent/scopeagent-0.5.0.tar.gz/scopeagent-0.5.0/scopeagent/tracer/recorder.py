"""
Originally derived from https://github.com/opentracing/basictracer-python.
"""
import threading

from abc import ABCMeta, abstractmethod
import six


class SpanRecorder(six.with_metaclass(ABCMeta, object)):
    """SpanRecorder is a simple abstract interface built around record_span.
    """

    def record_unfinished_span(self, span):
        pass

    def remove_unfinished_span(self, span):
        pass

    @abstractmethod
    def record_span(self, span):
        """After the call to finish(), each BasicSpan is passed as `span` to
        SpanRecorder.record_span.

        :param BasicSpan span: the finish()'d BasicSpan object.
        """
        pass


class InMemoryRecorder(SpanRecorder):
    """InMemoryRecorder stores all received spans in an internal list.

    This recorder is not suitable for production use, only for testing.
    """

    def __init__(self, metadata={}):
        self.spans = []
        self.mux = threading.Lock()
        self.metadata = metadata

    def record_span(self, span):
        with self.mux:
            self.spans.append(span)

    def get_spans(self):
        with self.mux:
            return self.spans[:]


class Sampler(six.with_metaclass(ABCMeta, object)):
    """Sampler determines the sampling status of a span given its trace_id.

    Sampler.sampled() is expected to return a boolean.
    """

    @abstractmethod
    def sampled(self, trace_id):
        pass


class DefaultSampler(Sampler):
    """DefaultSampler determines the sampling status via ID % rate == 0.
    """

    def __init__(self, rate):
        self.rate = rate

    def sampled(self, trace_id):
        return trace_id % self.rate == 0
