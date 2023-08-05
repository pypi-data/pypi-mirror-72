#!env python3
import sys
from fontTools.ttLib import TTFont
from argparse import ArgumentParser
import itertools

def main():
    parser = ArgumentParser(description="Interrogate a font")
    parser.add_argument("input", help="font file to process", metavar="FONT")
    parser.add_argument("-n", "--name", action="store_true", help="show font family name")
    parser.add_argument("-v", "--version", action="store_true", help="show font version")
    parser.add_argument("-c", "--count", action="store_true", help="show glyph count")
    parser.add_argument("-g", "--glyphset", action="store_true", help="show glyph names")
    parser.add_argument("-m", "--marks", action="store_true", help="show marks and bases")
    parser.add_argument("-M", "--metrics", action="store_true", help="show glyph metrics")
    parser.add_argument("--codepoints", action="store_true", help="show glyph codepoints")
    parser.add_argument(
        "--coverage", action="store_true", help="show Unicode coverage ranges"
    )
    parser.add_argument(
        "-l", "--layout", action="store_true", help="show OpenType layout information"
    )
    parser.add_argument(
        "--glyph-for",
        metavar="CHAR_OR_CODEPOINT",
        dest="glyphfor",
        help="show glyph name for given character or codepoint",
    )
    parser.add_argument("--all", action="store_true", help="show everything")

    args = parser.parse_args()
    font = TTFont(args.input)

    cmap = font["cmap"].getBestCmap()
    codepoints = list(cmap.keys())
    glyphset = font.getGlyphOrder()
    revcmap = font["cmap"].buildReversed()

    if len(sys.argv) < 3:
        args.name = True
        args.version = True
        args.count = True

    if args.codepoints or args.metrics:
        args.glyphset = True

    if args.glyphfor:
        if args.glyphfor.startswith("U+") or args.glyphfor.startswith("0x"):
            g = int(args.glyphfor[2:], 16)
        elif len(args.glyphfor) > 1:
            g = int(args.glyphfor, 16)
        else:
            g = ord(args.glyphfor)
        if not (g in cmap):
            print("U+%04X: not in font" % g)
        else:
            print("U+%04X -> %s" % (g, cmap[g]))


    def ranges(i):
        for a, b in itertools.groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
            b = list(b)
            yield b[0][1], b[-1][1]


    def categorize_glyph(font, glyphname):
        classdefs = font["GDEF"].table.GlyphClassDef.classDefs
        if not glyphname in classdefs:
            return ("base", None)
        if classdefs[glyphname] == 1:
            return ("base", None)
        if classdefs[glyphname] == 2:
            return ("ligature", None)
        if classdefs[glyphname] == 3:
            # Now find attachment class
            mclass = None
            if font["GDEF"].table.MarkAttachClassDef:
                markAttachClassDef = font["GDEF"].table.MarkAttachClassDef.classDefs
                mclass = markAttachClassDef[glyphname]
            return ("mark", mclass)
        if classdefs[glyphname] == 4:
            return ("component", None)


    def get_features(table, langSys):
        features = {}
        for featureIdx in langSys.FeatureIndex:
            featureRecord = table.FeatureList.FeatureRecord[featureIdx]
            featureTag = featureRecord.FeatureTag
            lookups = ", ".join([str(x) for x in featureRecord.Feature.LookupListIndex])
            features[featureTag] = lookups
        return features


    def show_layout_info_for_table(font, t):
        if t not in font:
            print("No %s table" % t)
            return

        table = font[t].table
        print("%s table: %i lookups" % (t, len(table.LookupList.Lookup)))
        for scriptRecord in table.ScriptList.ScriptRecord:
            scriptTag = scriptRecord.ScriptTag
            default = {}
            if scriptRecord.Script.DefaultLangSys is not None:
                print("%s/%s:" % (scriptTag, "dflt"))
                default = get_features(table, scriptRecord.Script.DefaultLangSys)
                for f, l in default.items():
                    print("    %s: %s" % (f, l))
            for langSysRecord in scriptRecord.Script.LangSysRecord:
                features = get_features(table, langSysRecord.LangSys)
                if features == default:
                    continue
                print("%s/%s:" % (scriptTag, langSysRecord.LangSysTag))
                for f, l in features.items():
                    if f in default and default[f] == l:
                        print("    %s: same as default" % f)
                        continue
                    print("    %s: %s" % (f, l))
        print("")


    if args.name or args.all:
        print("Name: %s" % font["name"].getDebugName(1))

    if args.version or args.all:
        print("Version: %s" % font["name"].getDebugName(5))

    if args.count or args.all:
        print("Glyph count: %i" % len(glyphset))

    if args.layout or args.all:
        show_layout_info_for_table(font, "GSUB")
        show_layout_info_for_table(font, "GPOS")

    if args.coverage or args.all:
        print("Codepoint coverage:")
        codepoints = list(cmap.keys())
        cplen = 4
        if list(filter(lambda x: x > 0xFFFF, codepoints)):
            cplen = 6

        def fmtcp(cp):
            return ("U+%0" + str(cplen) + "X") % cp

        cp_ranges = ranges(codepoints)
        for s, e in cp_ranges:
            if s == e:
                print(fmtcp(s), end=" ")
            else:
                print(fmtcp(s) + "-" + fmtcp(e), end=" ")
        print()

    if args.glyphset or args.all:
        print("Glyphs:")
        for ix, g in enumerate(glyphset):
            print("%12s" % g, end="")
            if args.marks or args.all:
                c, cx = categorize_glyph(font, g)
                if c == "mark":
                    print("[´]", end="")
                if c == "base":
                    print("   ", end="")
                if c == "ligature":
                    print("[ﬁ]", end="")
                if c == "component":
                    print("[◌]", end="")
            if args.codepoints or args.all:
                if g in revcmap:
                    for rc in revcmap[g]:
                        print(" U+%04X" % rc, end="")
            if args.metrics or args.all:
                advance, lsb = font["hmtx"][g]
                print(" advance=%i lsb=%i" % (advance, lsb), end="")
            if not args.metrics and not args.codepoints and not args.all:
                if ix % 5 == 0:
                    print("")
                else:
                    print(" ", end="")
            else:
                print("")

if __name__ == "__main__":
    main()