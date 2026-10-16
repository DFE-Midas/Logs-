# Stripe checkout setup

This version replaces the Google Maps calculator. No Google Maps key is needed. Postcodes.io provides coordinates without a key. Free delivery uses straight-line distance between the customer's postcode and WA15 0RB, up to 12 miles. All other postcodes use order enquiries and manually issued payment links. The supplier checks the 32-driving-mile limit and paid-delivery bands manually. Net orders require 20 log nets combined.

## Deployment

The STRIPE_SECRET_KEY variable must belong to the business and have Checkout Sessions write/read permissions plus permissions required by the one-off payments template. Restricted rk_ keys can be used. Start with a test key. Add the key through Netlify environment variables, not files. It must be available to production Functions. Deploy this complete folder using Git integration or Netlify CLI (netlify deploy --prod --dir . --functions netlify/functions), from inside this folder after linking the correct existing site. Ordinary drag-and-drop static uploads do not deploy these functions.

## Verification before real payments

Test eligible and outside-area postcodes, 19 vs 20 nets, out-of-stock ash, payment success and cancellation using Stripe test mode. Confirm delivery address, customer phone, postcode and itemised order appear in the Stripe Session/Payment metadata. The form's full delivery address is the delivery address; Stripe's address collection is the billing address. Make sure those are reviewed before fulfilment. Check the paid status in Stripe before dispatch. No automated fulfilment is implemented, so no webhook setup is required for this manual dispatch process. Do not rely on a customer's success-page screenshot.

Only switch the environment variable to the live key after test payments succeed, then redeploy. Enable payment notification emails in Stripe for the supplier. Real-payment end-to-end testing and deployment have not been completed by Codex. Delivery eligibility is recalculated server-side before Checkout and prices come from assets/catalogue.json. If product prices change, keep catalogue.json and products.js in sync.
