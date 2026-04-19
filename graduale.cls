% graduale.cls
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{graduale}[2026/01/14 Graduale/Gregorio class based on KOMA scrartcl]

% Rewrite paper=mantis -> paper=216mm:162mm, pass everything else through
\DeclareOption*{%
  \edef\graduale@opt{\CurrentOption}%
  \def\graduale@mantis{paper=mantis}%
  \ifx\graduale@opt\graduale@mantis
    \PassOptionsToClass{paper=216mm:162mm}{scrartcl}%
  \else
    \PassOptionsToClass{\CurrentOption}{scrartcl}%
  \fi
}
\ProcessOptions\relax

% Defaults (user options override these)
\LoadClass[10pt,parskip,DIV=calc]{scrartcl}



% ------------------------------------------------------------
% Packages
% ------------------------------------------------------------
\RequirePackage[osf,p]{libertine}
\RequirePackage[autocompile]{gregoriotex}
\RequirePackage[latin]{babel}
\RequirePackage{multicol}
\RequirePackage[margin=1cm]{geometry}
\RequirePackage{scrlayer-scrpage}
\RequirePackage{hyperref}

% ------------------------------------------------------------
% Paths / Gregorio
% ------------------------------------------------------------
\newcommand{\myhome}{C:/Users/johna/Chant/}
\gresetgregpath{{\myhome}}

% ------------------------------------------------------------
% Headings / page style
% ------------------------------------------------------------
\setkomafont{section}{\normalfont\centering\huge\scshape}
\setkomafont{subsection}{\normalfont\centering\Large\scshape}
\setkomafont{subsubsection}{\normalfont\centering\large\scshape}
\setcounter{secnumdepth}{-\maxdimen}

\setkomafont{pagehead}{\scshape}
\automark[section]{section}
\automark*[subsection]{subsection}
\pagestyle{scrheadings}

\RedeclareSectionCommand[
  runin=false,
  afterindent=false,
  beforeskip=0.75ex plus 1ex minus .2ex,
  afterskip=3pt
]{paragraph}

% ------------------------------------------------------------
% Gregorio layout tweaks
% ------------------------------------------------------------
\grechangedim{beforeinitialshift}{2.2mm}{scalable}
\grechangedim{afterinitialshift}{2.2mm}{scalable}

\gresetheadercapture{commentary}{grecommentary}{string}
\grechangedim{commentaryraise}{3.5mm}{scalable}

\grechangestyle{annotation}{\small\bfseries}

% ------------------------------------------------------------
% Utility: track missing files + make \label create anchors
% ------------------------------------------------------------
\newcounter{todos}
\setcounter{todos}{0}

\let\oldlabel\label
\renewcommand{\label}{\phantomsection\oldlabel}

\let\oldgregorioscore\gregorioscore
\renewcommand{\gregorioscore}[1]{%
  \IfFileExists{#1}{%
    \oldgregorioscore{#1}%
  }{%
    {\stepcounter{todos}\Large #1 (File does not exist)\\ }%
  }%
}

\endinput
