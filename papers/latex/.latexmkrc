#!/usr/bin/env perl

# https://qiita.com/ymfj/items/088fa556c94fc9ab460f#uplatex%E3%81%AE%E5%A0%B4%E5%90%88

$pdf_mode         = 3;
$latex            = 'uplatex -halt-on-error';
$latex_silent     = 'uplatex -halt-on-error -interaction=batchmode';
$bibtex           = 'upbibtex';
$dvipdf           = 'dvipdfmx %O -o %D %S';
$makeindex        = 'mendex %O -o %D %S';