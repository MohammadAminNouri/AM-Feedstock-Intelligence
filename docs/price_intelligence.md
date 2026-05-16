# Price intelligence policy

AM feedstock pricing is messy. This project avoids fake precision by separating evidence types.

## Price types

- `public_list`: public ecommerce/product page price.
- `request_quote`: supplier confirms product but does not publish price.
- `distributor_estimate`: site estimate or approximate price that may change before order.
- `marketplace`: weak signal from marketplace/aggregator.
- `manual_quote`: user-owned quote observation; do not publish confidential quote documents.

## Confidence rules

High confidence usually means:

- direct OEM/manufacturer or real quote
- date captured
- package size known
- product/SKU specific

Low confidence usually means:

- marketplace listing
- missing quantity
- missing manufacturer
- estimated price
- stale source

## Never average blindly

Do not average 10 g lab powder, 10 kg LPBF powder, 20 kg SLS powder, and 1 kg filament. Normalize only when package quantity and unit are clear. Keep quote-only products visible but without fake price.
