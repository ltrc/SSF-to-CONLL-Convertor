#!/usr/bin/env python

def is_projective(sent):
   proj=True
   spans = set()
   for tok in sent.split("\n"):
      tok = tok.split("\t")
      s = tuple(sorted([int(tok[0]), int(tok[6])]))
      spans.add(s)
   for l,h in sorted(spans):
      for l1,h1 in sorted(spans):
         if (l,h)==(l1,h1): continue
         if l < l1 < h and h1 > h:
            #print "non proj:",(l,h),(l1,h1)
            proj = False
   return proj

if __name__ == "__main__":

	import sys
	sentences = file(sys.argv[1]).read().strip().split("\n\n")
	rawSentences = file(sys.argv[2]).readlines()
	for idx, sentence in enumerate(sentences):
		if not sentence.strip():continue
		if not is_projective(sentence):
			print >> sys.stderr, "Sentence Number is >>", idx+1
			print >> sys.stderr, rawSentences[idx]
			print sentence;print
