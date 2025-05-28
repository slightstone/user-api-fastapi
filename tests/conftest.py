import os

import vcr

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "DUMMY_KEY")


def scrub_sensitive_data(request):
    if request.uri and API_KEY in request.uri:
        request.uri = request.uri.replace(API_KEY, "DUMMY_KEY")
    return request


my_vcr = vcr.VCR(
    cassette_library_dir="tests/cassettes",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
    filter_headers=["authorization"],
    before_record_request=scrub_sensitive_data,
    record_mode="once",  # only hits API the first time
)
