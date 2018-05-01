#!/bin/bash

. ./path.sh || exit 1
. ./cmd.sh || exit 1
 
nj=1       # number of parallel jobs - 1 is perfect for such a small data set
lm_order=1 # language model order (n-gram quantity) - 1 is enough for digits grammar
 
# Safety mechanism (possible running this script with modified arguments)
. utils/parse_options.sh || exit 1
[[ $# -ge 1 ]] && { echo "Wrong arguments!"; exit 1; }

utils/utt2spk_to_spk2utt.pl data/test/utt2spk > data/test/spk2utt
mfccdir=mfcc
steps/make_mfcc.sh --nj $nj --cmd "$train_cmd" data/test exp/make_mfcc/test $mfccdir
steps/compute_cmvn_stats.sh data/test exp/make_mfcc/test $mfccdir



echo
echo "===== TRI1 (first triphone pass) DECODING ====="
echo
 
utils/mkgraph.sh data/lang exp/tri1 exp/tri1/graph || exit 1
steps/decode.sh --config conf/decode.config --nj $nj --cmd "$decode_cmd" exp/tri1/graph data/test exp/tri1/decode
 
echo
echo "===== run.sh script is finished ====="
echo
