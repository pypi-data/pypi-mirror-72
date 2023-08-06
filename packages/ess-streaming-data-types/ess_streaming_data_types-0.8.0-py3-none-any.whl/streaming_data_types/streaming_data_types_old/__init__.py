from streaming_data_types.eventdata_ev42 import deserialise_ev42, serialise_ev42
from streaming_data_types.histogram_hs00 import deserialise_hs00, serialise_hs00
from streaming_data_types.logdata_f142 import deserialise_f142, serialise_f142
from streaming_data_types.nicos_cache_ns10 import deserialise_ns10, serialise_ns10
from streaming_data_types.run_start_pl72 import deserialise_pl72, serialise_pl72
from streaming_data_types.run_stop_6s4t import deserialise_6s4t, serialise_6s4t
from streaming_data_types.status_x5f2 import deserialise_x5f2, serialise_x5f2


SERIALISERS = {
    "ev42": serialise_ev42,
    "hs00": serialise_hs00,
    "f142": serialise_f142,
    "ns10": serialise_ns10,
    "pl72": serialise_pl72,
    "6s4t": serialise_6s4t,
    "x5f2": serialise_x5f2,
}


DESERIALISERS = {
    "ev42": deserialise_ev42,
    "hs00": deserialise_hs00,
    "f142": deserialise_f142,
    "ns10": deserialise_ns10,
    "pl72": deserialise_pl72,
    "6s4t": deserialise_6s4t,
    "x5f2": deserialise_x5f2,
}
