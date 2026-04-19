% ------------------------------------------------------------
% Options
% ------------------------------------------------------------
\newif\ifcb@pamphlet
\newif\ifcb@lect
\newif\ifcb@choir
\newif\ifcb@handout

% Intro layout control (non-choir only)
\newif\ifcb@introtext
\newif\ifcb@intrographic

% textonly option handling
\newif\ifcb@textonly
\newif\ifcb@textonlyset  % tracks whether user explicitly set it

% Defaults (raw defaults; textonly finalized after options are processed)
\cb@pamphletfalse
\cb@lectfalse
\cb@choirfalse
\cb@handouttrue

% intro=auto by default
\cb@introtextfalse
\cb@intrographicfalse

% textonly: not decided yet (will default based on pamphlet unless set)
\cb@textonlysetfalse

\newif\ifcb@nogloria
\cb@nogloriafalse

\DeclareOption{nogloria}{\cb@nogloriatrue}

\newif\ifcb@hymnset
\newif\ifcb@hymngraphic
\newif\ifcb@hymnshort
\newif\ifcb@hymnfull

\cb@hymnsetfalse
\cb@hymngraphicfalse
\cb@hymnshortfalse
\cb@hymnfullfalse


% --- Missing score behavior ---
% missingscore=warn: print a visible placeholder in the PDF
% missingscore=silent: print nothing (no placeholder)
% missingscore=error: keep gregorio's fatal behavior
\newif\ifcb@missingsilent
\newif\ifcb@missingwarn
\newif\ifcb@missingerror

% Default: silent
\cb@missingsilenttrue
\cb@missingwarnfalse
\cb@missingerrorfalse

\DeclareOption{missingscore=silent}{%
  \cb@missingsilenttrue
  \cb@missingwarnfalse
  \cb@missingerrorfalse
}
\DeclareOption{missingscore=warn}{%
  \cb@missingsilentfalse
  \cb@missingwarntrue
  \cb@missingerrorfalse
}
\DeclareOption{missingscore=error}{%
  \cb@missingsilentfalse
  \cb@missingwarnfalse
  \cb@missingerrortrue
}

\DeclareOption{pamphlet}{%
  \cb@pamphlettrue
}
\DeclareOption{lectionary}{%
  \cb@lecttrue
  \cb@handoutfalse
}
\DeclareOption{choir}{%
  \cb@choirtrue
  \cb@handoutfalse
}
\DeclareOption{handout}{%
  \cb@handouttrue
  \cb@lectfalse
  \cb@choirfalse
}

\DeclareOption{intro=text}{%
  \cb@introtexttrue
  \cb@intrographicfalse
}
\DeclareOption{intro=graphic}{%
  \cb@intrographictrue
  \cb@introtextfalse
}
\DeclareOption{intro=auto}{%
  \cb@introtextfalse
  \cb@intrographicfalse
}

% --- textonly option ---
% Supports: textonly, notextonly, textonly=true, textonly=false
\DeclareOption{textonly}{%
  \cb@textonlytrue
  \cb@textonlysettrue
}
\DeclareOption{notextonly}{%
  \cb@textonlyfalse
  \cb@textonlysettrue
}
\DeclareOption{textonly=true}{%
  \cb@textonlytrue
  \cb@textonlysettrue
}
\DeclareOption{textonly=false}{%
  \cb@textonlyfalse
  \cb@textonlysettrue
}

\DeclareOption{hymn=graphic}{%
  \cb@hymnsettrue
  \cb@hymngraphictrue
  \cb@hymnshortfalse
  \cb@hymnfullfalse
}
\DeclareOption{hymn=short}{%
  \cb@hymnsettrue
  \cb@hymngraphicfalse
  \cb@hymnshorttrue
  \cb@hymnfullfalse
}
\DeclareOption{hymn=full}{%
  \cb@hymnsettrue
  \cb@hymngraphicfalse
  \cb@hymnshortfalse
  \cb@hymnfulltrue
}

% Pass any other options through to scrartcl (MUST be last)
\DeclareOption*{%
  \PassOptionsToClass{\CurrentOption}{scrartcl}%
}

\ProcessOptions\relax

% If lectionary, force choir=true (per your original logic)
\ifcb@lect
  \cb@choirtrue
  \cb@handoutfalse
\fi

% Finalize textonly default:
% - default TRUE if pamphlet
% - default FALSE if not pamphlet
% - but if user set it explicitly, respect that
\ifcb@textonlyset\else
  \ifcb@pamphlet
    \cb@textonlytrue
  \else
    \cb@textonlyfalse
  \fi
\fi

\ifcb@hymnset\else
 \ifcb@pamphlet
   \cb@hymnshorttrue
 \fi
 \ifcb@handout
   \cb@hymnshorttrue
 \fi
 \ifcb@choir
   \cb@hymngraphictrue
 \fi
 \ifcb@lect
   \cb@hymngraphictrue
 \fi

\fi

% ------------------------------------------------------------
% Load base class + geometry based on pamphlet
% ------------------------------------------------------------
\ifcb@pamphlet
  \LoadClass[paper=8.5in:13.14in,parskip]{scrartcl}
\else
  \LoadClass[paper=letter,parskip]{scrartcl}
\fi

\RequirePackage{geometry}
\ifcb@pamphlet
  \geometry{margin=0.5cm}
\else
  \geometry{margin=1.5cm}
\fi

% ------------------------------------------------------------
% Packages (from your preamble)
% ------------------------------------------------------------
\RequirePackage[osf,p]{libertine}
\RequirePackage[autocompile]{gregoriotex}
\RequirePackage[latin]{babel}
\RequirePackage{multicol}
\RequirePackage{scrlayer-scrpage}
\RequirePackage{xargs}
\RequirePackage{soul}
\RequirePackage{graphicx} % needed for \includegraphics used in \introd
\RequirePackage{etoolbox} % needed for string comparison

% ------------------------------------------------------------
% Public toggles (match your names)
% ------------------------------------------------------------
\newif\iflect
\newif\ifchoir
\newif\iftextonly
\newif\ifhymngraphic
\newif\ifhymnshort
\newif\ifhymnfull
\newif\ifnogloria


% Apply option-driven defaults:
\ifcb@lect \lecttrue \else \lectfalse \fi
\ifcb@choir \choirtrue \else \choirfalse \fi

% textonly is now driven entirely by the class option logic above
\ifcb@textonly \textonlytrue \else \textonlyfalse \fi

\ifcb@hymngraphic \hymngraphictrue \else \hymngraphicfalse \fi
\ifcb@hymnshort \hymnshorttrue \else \hymnshortfalse \fi
\ifcb@hymnfull \hymnfulltrue \else \hymnfullfalse \fi
\ifcb@nogloria \nogloriatrue \else \nogloriafalse \fi


% ------------------------------------------------------------
% Your settings/macros
% ------------------------------------------------------------
% ------------------------------------------------------------
% Missing-score handling for Gregorio (prevents fatal error unless requested)
% ------------------------------------------------------------
\let\loth@oldgregorioscore\gregorioscore

\newcommand{\flex}{†\\}
\newcommand{\mediant}{*\\}

\newcommand{\loth@missingscore}[1]{%
  \ifcb@missingerror
    % Call original gregorio (will error)
    \loth@oldgregorioscore{#1}%
  \else\ifcb@missingsilent
    % Do nothing
  \else
    % warn (default): visible placeholder
    {\par\noindent\Large\ttfamily Missing score: #1\par\normalfont}%
  \fi\fi
}

\newcommand{\maybeinput}[1]{%
\IfFileExists{#1}{
  \input{#1}%
}{%
  \ifcb@missingerror
    % Call input anyway (will error)
    \input{#1}%
  \else\ifcb@missingsilent
    % Do nothing
  \else
    % warn (default): visible placeholder
    {\par\noindent\Large\ttfamily Missing file: #1\par\normalfont}%
  \fi\fi
}%
}

\renewcommand{\gregorioscore}[1]{%
  \IfFileExists{#1}{%
    \loth@oldgregorioscore{#1}%
  }{%
    \loth@missingscore{#1}%
  }%
}


\newcommand{\myhome}{C:/Users/johna/Dropbox/Chant/}
\gresetgregpath{{\myhome}}

\setcounter{secnumdepth}{-\maxdimen} % remove section numbering

\setkomafont{pagehead}{\scshape}

\sethlcolor{white}
\let\oldhl\hl
\renewcommand{\hl}[1]{\ifchoir \oldhl{#1} \else #1 \fi}

\newcounter{antcnt}
\setcounter{antcnt}{1}
\newcounter{lessoncnt}
\setcounter{lessoncnt}{1}

\setlength{\multicolsep}{0.5ex}

\setkomafont{section}{\normalfont\centering\huge\scshape\bfseries}
\setkomafont{subsection}{\normalfont\centering\large\scshape}
\setkomafont{subsubsection}{\normalfont\centering\small\scshape}
\setkomafont{paragraph}{\normalfont\small\bfseries}

\iftextonly
  \RedeclareSectionCommand[
      runin=true,
      beforeskip=0.25ex plus 1ex minus .2ex
  ]{paragraph}
  \RedeclareSectionCommand[
      afterindent=false,
      beforeskip=.05\baselineskip,
      afterskip=.05\baselineskip
  ]{subsubsection}
  \RedeclareSectionCommand[
      afterindent=false,
      beforeskip=.05\baselineskip,
      afterskip=.05\baselineskip
  ]{subsection}
  \RedeclareSectionCommand[
      afterindent=false,
      beforeskip=.05\baselineskip,
      afterskip=.05\baselineskip
  ]{section}
  \setkomafont{subsubsection}{\normalfont\centering\scshape}
\else
\RedeclareSectionCommand[
      runin=false,
      afterindent=false,
      beforeskip=3.25ex plus 1ex minus .2ex,
      afterskip=3pt
  ]{paragraph}
  \RedeclareSectionCommand[
      afterindent=false,
      beforeskip=.25\baselineskip,
      afterskip=.15\baselineskip
  ]{subsubsection}
  \RedeclareSectionCommand[
      afterindent=false,
      beforeskip=.15\baselineskip,
      afterskip=.05\baselineskip
  ]{subsection}
  \RedeclareSectionCommand[
      afterindent=false,
      beforeskip=.25\baselineskip,
      afterskip=.15\baselineskip
  ]{section}
\fi

% Gregorio layout tweaks
\grechangedim{beforeinitialshift}{2.2mm}{scalable}
\grechangedim{afterinitialshift}{2.2mm}{scalable}

\gresetheadercapture{commentary}{grecommentary}{string}
\grechangedim{commentaryseparation}{0.15mm}{scalable}

\grechangestyle{annotation}{\small\bfseries}

% ------------------------------------------------------------
% Psalm tone → syllable-pattern category lookup
% Edit this table to add or change mappings.
% Key  = tone string as passed to \psalm arg3 (or \psalma arg4)
% Sets \loth@ts to the category code (e.g. 1-0-1-2) as a plain string.
% Call as \loth@settonecat{tone} — do NOT use inside \edef.
% ------------------------------------------------------------
\newcommand{\loth@settonecat}[1]{%
  % ---- Tone 1 ----
  \ifstrequal{#1}{1g}    {\def\loth@ts{2-0-1-2}}{%
  \ifstrequal{#1}{1f}    {\def\loth@ts{2-0-1-2}}{%
  \ifstrequal{#1}{1d2}   {\def\loth@ts{2-0-1-2}}{%
  \ifstrequal{#1}{1g-sol}{\def\loth@ts{1-3-1-2}}{% Magnificat variant
  % ---- Tone 2 ----
  \ifstrequal{#1}{2d}    {\def\loth@ts{1-0-1-1}}{%
  \ifstrequal{#1}{2alta} {\def\loth@ts{1-2-1-3}}{%
  % ---- Tone 3 ----
  \ifstrequal{#1}{3a}    {\def\loth@ts{2-0-2-0}}{%
  \ifstrequal{#1}{3b}    {\def\loth@ts{2-0-2-0}}{%
  % ---- Tone 4 ----
  \ifstrequal{#1}{4a}    {\def\loth@ts{1-2-1-3}}{%
  \ifstrequal{#1}{4alta} {\def\loth@ts{1-2-1-3}}{%
  \ifstrequal{#1}{4e}    {\def\loth@ts{1-2-1-3}}{%
  \ifstrequal{#1}{D}     {\def\loth@ts{1-2-1-3}}{%
  % ---- Tone 5 ----
  \ifstrequal{#1}{5a}    {\def\loth@ts{1-0-2-0}}{%
  % ---- Tone 6 ----
  \ifstrequal{#1}{6}     {\def\loth@ts{1-1-1-2}}{%
  % ---- Tone 7 ----
  \ifstrequal{#1}{7a}    {\def\loth@ts{2-0-2-0}}{%
  \ifstrequal{#1}{7c}    {\def\loth@ts{2-0-2-0}}{%
  \ifstrequal{#1}{7c2}   {\def\loth@ts{2-0-2-0}}{%
  \ifstrequal{#1}{7d}    {\def\loth@ts{2-0-2-0}}{%
  % ---- Tone 8 ----
  \ifstrequal{#1}{8c}    {\def\loth@ts{1-0-1-2}}{%
  \ifstrequal{#1}{8g}    {\def\loth@ts{1-0-1-2}}{%
  \ifstrequal{#1}{8G}    {\def\loth@ts{1-0-1-2}}{%
  \ifstrequal{#1}{8g2}   {\def\loth@ts{1-0-1-2}}{%
  % ---- Tonus Peregrinus ----
  \ifstrequal{#1}{per}   {\def\loth@ts{per}}{%
  \PackageWarning{loth}{Unknown psalm tone '#1': no default category; pass it explicitly}%
  \def\loth@ts{#1}%
  }}}}}}}}}}}}}}}}}}}}}}}%
}

% ------------------------------------------------------------
% Your document-level commands
% ------------------------------------------------------------

\newcommandx{\hymn}[5][4=english,5=0.85]{
\subsubsection*{Hymn: ``#2'' \hfill
{\small\itshape #3}}
\ifhymngraphic
\begin{center}
    \includegraphics[width=#5\textwidth]{hymns/#1/formatted.png}
\end{center}
\fi%
\ifhymnfull
\gregorioscore{hymns/#1/#4.gabc}
\fi%
\ifhymnshort
\gregorioscore{hymns/#1/#4_v1.gabc}
   \begin{multicols}{2}
       \iftextonly\Large\else\small\fi
       \maybeinput{\myhome/hymns/#1/verses.tex}
   \end{multicols}
\fi
}

\newcommand{\introd}[1]{%
  \marginpar{\small\scshape Stand}%
  \ifchoir
    \gregorioscore{Communes/deus-in-adjutorium/#1.gabc}%
  \else
    % Decide which non-choir intro layout to use based on class options
    \ifcb@introtext
      \emph{God, come to my assistance. --\textbf{LORD, make haste to help me.}\\
      Glory be to the Father, and to the Son, and to the Holy Spirit.
      --\textbf{As it was in the beginning, is now, and ever shall be, world with out end. Amen. Alleluia.}}%
    \else
      % intro=graphic or intro=auto (default)
      \begin{minipage}{0.39\textwidth}%
        \includegraphics[width=0.95\textwidth]{Communes/deus-in-adjutorium/#1-condensed.png}%
      \end{minipage}\hfill
      \begin{minipage}{0.59\textwidth}%
        \begin{center}%
        \emph{God, come to my assistance. --\textbf{LORD, make haste to help me.}\\
        Glory be to the Father, and to the Son, and to the Holy Spirit.
        --\textbf{As it was in the beginning, is now, and ever shall be, world with out end. Amen. Alleluia.}}%
        \end{center}%
      \end{minipage}%
    \fi
  \fi
}


% Internal helper: render psalm tone score + text columns
% \loth@psalmchoir{psalm}{tone}{repeat-text}
%   repeat-text is appended inside multicols (e.g. \emph{The Latin antiphon is repeated.})
\newread\loth@titleread
\NewDocumentCommand{\loth@psalmchoir}{m m m}{%
  % Pre-read the title to avoid passing \input{} directly to \paragraph
  % (KOMA passes the short-title argument raw into \setkeys, so \input would
  %  be executed in that context and cause "Illegal parameter number".)
  \ifchoir
    \gregorioscore{Psalms/#1/#2.gabc}%
    \nopagebreak%
    \begin{multicols}{2}%
      \raggedcolumns
      \small
      \maybeinput{\myhome/Psalms/#1/\loth@ts.tex}
      
      \ifcb@nogloria\else\maybeinput{\myhome/Psalms/GloriaPatri/\loth@ts.tex}\fi
      
      #3%
    \end{multicols}%
  \else
    \begin{multicols}{2}%
      \iftextonly\Large\else\small\fi
      \maybeinput{\myhome/Psalms/#1/all.tex}%
      #3%
    \end{multicols}%
  \fi
}

% \psalm{antiphon}{psalm}{tone}{tonecat}[version]
%   tonecat is optional: omit (or pass {}) to auto-derive from tone via \loth@tonecat
%   version defaults to "solesmes"
\NewDocumentCommand{\psalm}{m m m G{} O{solesmes}}{%
  \IfFileExists{Psalms/#1/title.tex}{%
    \openin\loth@titleread={Psalms/#1/title.tex}%
    \read\loth@titleread to\loth@psalmmtitle
    \closein\loth@titleread
    \paragraph{\loth@psalmmtitle}
  }{%
  }%
      \ifdefstring{#5}{english}%
      {}%
      {%
        \IfFileExists{Antiphona/#1/english.gabc}{%
          %\gregorioscore{Antiphona/#1/english.gabc}%
        }{%
          \ifcb@missingsilent
            \def\loth@repant{\emph{The antiphon is repeated.}}
          \else
            %\loth@missingscore{Antiphona/#1/english.gabc}%
          \fi
        }%
      }%
    \let\olditem\item % Someday will refactor to wrap psalm content in itemize
    \renewcommand{\item}{} % Ignore \item for now so psalms using new format work with the old flow
  \ifblank{#4}{\loth@settonecat{#3}}{\def\loth@ts{#4}}% resolve tone structure
  \iftextonly
    \textbf{\Large Ant \theantcnt: \maybeinput{Antiphona/#1/english.txt}}\\
    \textbf{Ant: \maybeinput{Antiphona/#1/#5.txt}}%
  \else
    \greannotation{Ant. \theantcnt}%
    \greannotation{#3}%
    \gregorioscore{Antiphona/#1/#5.gabc}%
  \fi
  \gresetinitiallines{0}%
  \loth@psalmchoir{#2}{#3}{\loth@repant}%
  \def\loth@repant{}
  \iftextonly
    % (no English antiphon score in text-only mode)
  \else
    \ifdefstring{#5}{english}%
      {\emph{The antiphon is repeated.}}%
      {%
        \IfFileExists{Antiphona/#1/english.gabc}{%
          \gregorioscore{Antiphona/#1/english.gabc}%
        }{%
          \ifcb@missingsilent
            % \begin{multicols}{2}%
            %   \emph{The antiphon is repeated.}%
            % \end{multicols}%
          \else
            \loth@missingscore{Antiphona/#1/english.gabc}%
          \fi
        }%
      }%
  \fi
  \gresetinitiallines{1}%
  \stepcounter{antcnt}%
  \renewcommand{\item}{\olditem} % Restore \item
}

% \psalma{latinant}{engant}{psalm}{tone}{tonecat}[version]
%   tonecat is optional: omit (or pass {}) to auto-derive from tone via \loth@tonecat
%   version defaults to "solesmes"
\NewDocumentCommand{\psalma}{m m m m G{} O{solesmes}}{%
  \IfFileExists{Psalms/#1/title.tex}{%
    \openin\loth@titleread={Psalms/#1/title.tex}%
    \read\loth@titleread to\loth@psalmmtitle
    \closein\loth@titleread
    \paragraph{\loth@psalmmtitle}
  }{%
  }%
    \let\olditem\item % Someday will refactor to wrap psalm content in itemize
    \renewcommand{\item}{} % Ignore \item for now so psalms using new format work with the old flow
  \ifblank{#5}{\loth@settonecat{#4}}{\def\loth@ts{#5}}% resolve tone structure
  \iftextonly
    \textbf{\Large Ant \theantcnt: \maybeinput{Antiphona/#1/#6.txt}}%
  \else
    \greannotation{Ant. \theantcnt}%
    \greannotation{#4}%
    \gregorioscore{Antiphona/#1/#6.gabc}%
  \fi
  \gresetinitiallines{0}%
  \iftextonly\else
    \gregorioscore{antiphons-english/#2/english.gabc}%
  \fi
  \loth@psalmchoir{#3}{#4}{\emph{The Latin antiphon is repeated.}}%
  \gresetinitiallines{1}%
  \stepcounter{antcnt}%
  \renewcommand{\item}{\olditem} % Restore \item
}


\newcommandx{\responsory}[2][2=english]{%
  \subsubsection{Responsory}%
  \ifchoir
    \gregorioscore{Resp-breve/#1/#2-extended.gabc}%
  \else
    \iftextonly
      \maybeinput{Resp-breve/#1/#2.tex}%
    \else
      \gregorioscore{Resp-breve/#1/#2.gabc}%
    \fi
  \fi
}

\newcommandx{\lesson}[2]{
  \subsubsection{Lesson \roman{lessoncnt}: #2}%
  \iflect % Use pointed if possible
    \IfFileExists{Lectionis/#1.gabc}{%
      \gregorioscore{Lectionis/#1.gabc}%
    }{%
      \maybeinput{Lectionis/#1.tex}%
    }%
  \else % Use text if possible
    \IfFileExists{Lectionis/#1.tex}{%
      \maybeinput{Lectionis/#1.tex}%
    }{%
      \gregorioscore{Lectionis/#1.gabc}%
    }%
  \fi
  \stepcounter{lessoncnt}%
}

\endinput
