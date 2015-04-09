USAGE:
```
bash ssf2conll.sh file/directory output file log file"
```
Input Data can either be a file or a folder.

The data should be in ssf format. Inter-Chunk dependecies should be formatted as in the following:
```
<Sentence id='10'>
1       ((      NP      <fs name='NP' drel='k1:VGF'>
1.1     mEM     PRP     <fs af='mEM,pn,any,sg,1,d,0,0' name='mEM' posn='10'>
1.2     wo      RP      <fs af='wo,avy,,,,,,' name='wo' posn='20'>
        ))
2       ((      NP      <fs name='NP2' drel='k1s:VGF'>
2.1     axanA   JJ      <fs af='axanA,adj,m,sg,,d,,' name='axanA' posn='30'>
2.2     sA      RP      <fs af='sA,avy,m,sg,,d,,' name='sA' posn='40'>
2.3     iMsAna  NN      <fs af='iMsAna,n,m,sg,3,d,0,0' name='iMsAna' posn='50'>
        ))
3       ((      VGF     <fs name='VGF' stype='declarative' voicetype='active'>
3.1     hUM     VM      <fs af='hE,v,any,sg,1,,hE,hE' name='hUM' posn='60'>
        ))
4       ((      BLK     <fs name='BLK' drel='rsym:VGF'>
4.1     .       SYM     <fs af='.,punc,,,,,,' name='.' posn='70'>
        ))
</Sentence>
```
While Intra-chunk dependencies should be in the following SSF format:
```
<Sentence id="2">
1       Kusa    JJ      <fs af='Kusa,adj,any,any,,,,' drel='pof:raha' posn='10' name='Kusa' chunkId='JJP' chunkType='head:JJP'>
2       raha    VM      <fs af='raha,v,any,sg,2,,0,0' stype='declarative' posn='20' voicetype='active' name='raha' chunkId='VGF' chunkType='head:VGF'>
3       XUlIcanxa       NNP     <fs af='XUlIcanxa,n,m,sg,3,d,0,0' drel='rad:raha' posn='30' name='XUlIcanxa' chunkId='NP' chunkType='head:NP'>
4       .       SYM     <fs af='.,punc,,,,,,' drel='rsym:raha' posn='40' name='.' chunkId='BLK' chunkType='head:BLK'>
</Sentence>
```
Dependencies are:
```
1. headcomputation
2. vibhakticomputation
```
Set the environment variable ssf2conll to conll converter folder in ~/.bashrc as 
```
export ssf2conll="PATH OF CONLL CONVERTER FOLDER"
```
