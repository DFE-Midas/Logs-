# Altrincham Firewood & Coal Supplier

A complete buildless website for Netlify. No npm install, build process or external image service is needed. All photography and product assets are included locally.

## Included

Home, Shop, Delivery, About Us, Contact, Basket, Privacy, Thank You and 404 pages; responsive navigation; 18-product catalogue with category filters and sorting; persistent browser basket with quantity updates, removal and product subtotals; itemised order enquiries; Netlify contact forms; SEO metadata and LocalBusiness structured data.

## Deploy a preview on Netlify

1. Unzip this package.
2. Upload the contents of this folder to Netlify, or connect a repository containing these files. `index.html` must be at the published root.
3. Build command: leave blank. Publish directory: `.`. The included `netlify.toml` sets this.
4. In the Netlify project, enable form detection under Forms if it is not already enabled, then redeploy. Confirm `contact` and `order-enquiry` are detected.
5. Under Forms / form notifications, add the supplier's confirmed recipient email. The website email links do not automatically configure notification delivery.
6. Submit one contact enquiry and one multi-product basket enquiry on the actual Netlify URL. Check that both are received in Forms, the itemised order is complete, the notification arrives, and the thank-you page opens only after submission succeeds.

Form processing requires Netlify. Opening the files directly is suitable for browsing and trying the basket, but will not submit a real enquiry. No payment gateway is connected: customers submit requests and the supplier confirms the final order.

## Prices checked 13 October 2026

The live `.com` all-products page and the live `.co.uk` product pages were fetched directly. Search-engine snapshots returned older values, so direct pages were used. Current main prices agree between the live sites: XL ash/oak nets £10; bulk ash/oak £130; bulk birch £125; standard birch net £7.50. The `.com` catalogue supplies the mixed bags, accessories and 25 kg coal. The `.co.uk` site supplies the 30 litre ash net (£7.50), barn dried bag (£105) and 20 kg coal (£15).

Full sources, product names, units and prices appear in `price-sources.json`. One duplicated mixed-hardwood bulk-bag listing was consolidated. Bulk bags are labelled by approximate 1 m³ volume, not by a guaranteed weight. Photographs for the 30 litre ash net, barn dried bag and 20 kg coal illustrate their product category using an existing related listing; replace these with exact pack photographs before launch if the supplier has them.

Run `python3 tools/verify-prices.py` to re-check the live listings. It reports differences rather than automatically changing selling prices. Public pages can change independently of real stock or the supplier's intended price list. Have the supplier confirm the entire catalogue, prices, minimum orders, current fuel specifications, delivery terms and recipient email before public launch. Contact email links currently use the `.com` site's published `enquiries@altrinchamlogs.com`; the `.co.uk` site publishes a different address, so confirm which mailbox should be used.

## Public launch and SEO

This updated package is configured for https://logsforsalemanchester.co.uk with indexing enabled, canonical links, Open Graph metadata, a sitemap, LocalBusiness, FAQ and breadcrumb structured data. Basket, thank-you and error pages remain excluded from indexing.

If the final domain changes, run:

    python3 tools/prepare-launch.py https://YOUR-CONFIRMED-DOMAIN

This adds page-specific canonical links, absolute Open Graph images and URLs, creates a sitemap, updates robots.txt, and removes the preview noindex directives. Use the final domain, including https://. Upload/redeploy the resulting folder. Do not change the existing domain's DNS until the Netlify site, forms and prices are verified. Submit the sitemap in Search Console after connecting the intended domain.

Basket and thank-you pages remain noindex. The supplier should complete its own privacy retention details, business identity/address and ordering terms before accepting confirmed orders. The included privacy page describes the actual enquiry-only workflow; no analytics, marketing cookies or payment collection are installed.

## Editing

- Design: `assets/style.css`.
- Basket and navigation: `assets/app.js`.
- Product data: `assets/products.js` (prices are integer pence).
- Visible product cards: `shop.html` and selected cards in `index.html`. If product data changes, update the visible cards as well, then run `tools/check-site.py` to check consistency.
- Contact details and copy: individual HTML files.
- Asset credits: `ASSET-CREDITS.md`.

## Verification completed

JavaScript syntax checks; execution checks for basket persistence, invalid stored values, exact totals, itemised POST payload and submission success handling; local file and link checks; product catalogue/card price consistency; HTML metadata and heading checks; asset decoding. Wood-burner photography has been added to the homepage; decorative section numbers have been removed throughout.

Browser viewport/interactivity testing and live Netlify form delivery were not available in this build environment. Complete the live deployment checks above before launch.
