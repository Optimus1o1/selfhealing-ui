"""
Self-Contained E-Commerce Demonstration Application (V1 vs V2).
Moon Sanctum Labs — Decode. Build. Evolve.

Provides two complete versions of a multi-page e-commerce store:
- Version 1 (V1): Baseline DOM structure, clean semantic IDs, and classic CSS classes.
- Version 2 (V2): Refactored DOM with intentional UI mutations:
  * Renamed IDs (kebab, camel, snake, generated hash)
  * Changed CSS classes (Bootstrap -> Tailwind utility classes)
  * Semantic text variations ("Login" -> "Sign In", "Add to Cart" -> "Add to Bag", "Proceed to Checkout" -> "Continue to Payment")
  * DOM hierarchy restructuring (nested wrappers, fieldsets, sticky action bars)
  * Repeated accessible names across product cards (context disambiguation)
  * Dynamic async hydration (simulated cart updates)
  * Near-tie ambiguous collisions (for negative rejection verification)
  * Actionability states (disabled checkout button without terms)

Pages provided for both V1 and V2:
1. /ecommerce/vX/login
2. /ecommerce/vX/register
3. /ecommerce/vX/products
4. /ecommerce/vX/cart
5. /ecommerce/vX/checkout
6. /ecommerce/vX/order-success
7. /ecommerce/vX/ambiguous-demo (Ambiguity rejection test page)
"""

# =============================================================================
# VERSION 1 (BASELINE) HTML TEMPLATES
# =============================================================================

V1_NAVBAR = """
<header id="siteHeader" class="site-header">
    <nav id="mainNav" class="navbar">
        <div class="nav-brand"><a href="/ecommerce/v1/products" id="brandLogo">MoonStore V1</a></div>
        <div class="nav-search">
            <input type="text" id="navSearchInput" placeholder="Search catalog..." />
            <button type="button" id="btnSearch" class="btn-search">Search</button>
        </div>
        <div class="nav-links">
            <a href="/ecommerce/v1/products" id="navProductsLink">Products</a>
            <a href="/ecommerce/v1/cart" id="navCartLink">Cart (<span id="cartCount">2</span>)</a>
            <a href="/ecommerce/v1/login" id="navLoginLink">Login</a>
        </div>
    </nav>
</header>
"""

V1_STYLES = """
<style>
    * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    body { margin: 0; background: #f8fafc; color: #1e293b; }
    .site-header { background: #0f172a; color: white; padding: 1rem 2rem; }
    .navbar { display: flex; justify-content: space-between; align-items: center; max-width: 1100px; margin: 0 auto; }
    .nav-brand a { color: #f8fafc; font-size: 1.25rem; font-weight: bold; text-decoration: none; }
    .nav-search { display: flex; gap: 0.5rem; }
    .nav-search input { padding: 6px 12px; border-radius: 4px; border: 1px solid #475569; }
    .btn-search { background: #3b82f6; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
    .nav-links a { color: #cbd5e1; margin-left: 1.5rem; text-decoration: none; font-weight: 500; }
    .container { max-width: 1000px; margin: 2rem auto; padding: 0 1rem; }
    .card { background: white; border-radius: 8px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 1.5rem; }
    .form-group { margin-bottom: 1rem; }
    .form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
    .form-group input { width: 100%; padding: 8px 12px; border: 1px solid #cbd5e1; border-radius: 4px; }
    .btn { display: inline-block; padding: 10px 18px; border-radius: 4px; font-weight: 600; cursor: pointer; text-align: center; border: none; text-decoration: none; }
    .btn-primary { background: #2563eb; color: white; }
    .btn-secondary { background: #64748b; color: white; }
    .btn-success { background: #16a34a; color: white; }
    .btn-danger { background: #dc2626; color: white; }
    .product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }
    .product-card { background: white; border-radius: 8px; padding: 1.25rem; border: 1px solid #e2e8f0; display: flex; flex-direction: column; justify-content: space-between; }
    .product-price { font-size: 1.25rem; font-weight: bold; color: #0f172a; margin: 0.5rem 0; }
    .cart-table { width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; }
    .cart-table th, .cart-table td { padding: 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }
    .badge { background: #e2e8f0; padding: 2px 8px; border-radius: 9999px; font-size: 0.8rem; }
</style>
"""

V1_LOGIN_HTML = f"""<!DOCTYPE html>
<html>
<head><title>Login - MoonStore V1</title>{V1_STYLES}</head>
<body>
{V1_NAVBAR}
<div class="container" style="max-width: 420px;">
    <div class="card">
        <h2>Customer Sign In</h2>
        <p style="color: #64748b; font-size: 0.9rem;">Sign in to access your orders and checkout.</p>
        <form action="/ecommerce/v1/products" method="GET" id="loginForm">
            <div class="form-group">
                <label for="username">Username / Email</label>
                <input type="text" id="username" name="username" placeholder="john.doe@example.com" required />
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Enter secure password" required />
            </div>
            <button type="submit" id="btnLogin" class="btn btn-primary" style="width: 100%;">Login</button>
        </form>
        <div style="margin-top: 1rem; text-align: center; font-size: 0.9rem;">
            Don't have an account? <a href="/ecommerce/v1/register" id="linkRegister">Register here</a>
        </div>
    </div>
</div>
</body></html>"""

V1_REGISTER_HTML = f"""<!DOCTYPE html>
<html>
<head><title>Register - MoonStore V1</title>{V1_STYLES}</head>
<body>
{V1_NAVBAR}
<div class="container" style="max-width: 480px;">
    <div class="card">
        <h2>Create Account</h2>
        <form action="/ecommerce/v1/products" method="GET" id="registerForm">
            <div class="form-group">
                <label for="fullName">Full Name</label>
                <input type="text" id="fullName" name="fullName" placeholder="Jane Doe" required />
            </div>
            <div class="form-group">
                <label for="regEmail">Email Address</label>
                <input type="email" id="regEmail" name="email" placeholder="jane@example.com" required />
            </div>
            <div class="form-group">
                <label for="regPassword">Password</label>
                <input type="password" id="regPassword" name="password" placeholder="Create password" required />
            </div>
            <button type="submit" id="btnRegisterSubmit" class="btn btn-primary" style="width: 100%;">Register</button>
        </form>
    </div>
</div>
</body></html>"""

V1_PRODUCTS_HTML = f"""<!DOCTYPE html>
<html>
<head><title>Product Catalog - MoonStore V1</title>{V1_STYLES}</head>
<body>
{V1_NAVBAR}
<div class="container">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
        <h2>Featured Products</h2>
        <span class="badge" id="productCountBadge">3 Items Available</span>
    </div>
    <div class="product-grid">
        <!-- Product 1 -->
        <div class="product-card" id="cardProduct1" data-product-id="101">
            <div>
                <h3 class="product-title">Quantum Mechanical Keyboard</h3>
                <p style="color: #64748b; font-size: 0.9rem;">Ultra-responsive tactile optical switches.</p>
                <div class="product-price">$149.99</div>
            </div>
            <div style="margin-top: 1rem;">
                <button type="button" id="btnAddToCart1" class="btn btn-primary" aria-label="Add Quantum Mechanical Keyboard to Cart" style="width: 100%;" onclick="window.location='/ecommerce/v1/cart'">Add to Cart</button>
            </div>
        </div>
        <!-- Product 2 -->
        <div class="product-card" id="cardProduct2" data-product-id="102">
            <div>
                <h3 class="product-title">Ergonomic Precision Mouse</h3>
                <p style="color: #64748b; font-size: 0.9rem;">Wireless Bluetooth 26,000 DPI sensor.</p>
                <div class="product-price">$89.99</div>
            </div>
            <div style="margin-top: 1rem;">
                <button type="button" id="btnAddToCart2" class="btn btn-primary" aria-label="Add Ergonomic Precision Mouse to Cart" style="width: 100%;" onclick="window.location='/ecommerce/v1/cart'">Add to Cart</button>
            </div>
        </div>
        <!-- Product 3 -->
        <div class="product-card" id="cardProduct3" data-product-id="103">
            <div>
                <h3 class="product-title">Noise-Cancelling Studio Headset</h3>
                <p style="color: #64748b; font-size: 0.9rem;">Planar magnetic high-fidelity drivers.</p>
                <div class="product-price">$249.99</div>
            </div>
            <div style="margin-top: 1rem;">
                <button type="button" id="btnAddToCart3" class="btn btn-primary" aria-label="Add Noise-Cancelling Studio Headset to Cart" style="width: 100%;" onclick="window.location='/ecommerce/v1/cart'">Add to Cart</button>
            </div>
        </div>
    </div>
</div>
</body></html>"""

V1_CART_HTML = f"""<!DOCTYPE html>
<html>
<head><title>Shopping Cart - MoonStore V1</title>{V1_STYLES}</head>
<body>
{V1_NAVBAR}
<div class="container">
    <div class="card">
        <h2>Your Shopping Cart</h2>
        <table class="cart-table">
            <thead>
                <tr><th>Item</th><th>Qty</th><th>Price</th><th>Subtotal</th></tr>
            </thead>
            <tbody>
                <tr><td>Quantum Mechanical Keyboard</td><td>1</td><td>$149.99</td><td>$149.99</td></tr>
                <tr><td>Ergonomic Precision Mouse</td><td>1</td><td>$89.99</td><td>$89.99</td></tr>
            </tbody>
        </table>
        
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="display: flex; gap: 0.5rem;">
                <input type="text" id="promoCodeInput" placeholder="Promo code (SAVE10)" style="padding: 8px;" />
                <button type="button" id="btnApplyPromo" class="btn btn-secondary">Apply Coupon</button>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 1rem;" id="cartTotalText">Total: $239.98</div>
                <a href="/ecommerce/v1/checkout" id="btnProceedCheckout" class="btn btn-success" style="padding: 12px 24px; font-size: 1.1rem;">Proceed to Checkout</a>
            </div>
        </div>
    </div>
</div>
</body></html>"""

V1_CHECKOUT_HTML = f"""<!DOCTYPE html>
<html>
<head><title>Checkout - MoonStore V1</title>{V1_STYLES}</head>
<body>
{V1_NAVBAR}
<div class="container" style="max-width: 700px;">
    <div class="card">
        <h2>Order Checkout</h2>
        <form action="/ecommerce/v1/order-success" method="GET" id="checkoutForm">
            <h3>1. Shipping Address</h3>
            <div class="form-group">
                <label for="shippingAddress">Street Address</label>
                <input type="text" id="shippingAddress" name="address" placeholder="123 Tech Boulevard" required />
            </div>
            <div class="form-group">
                <label for="shippingCity">City</label>
                <input type="text" id="shippingCity" name="city" placeholder="Kolkata" required />
            </div>

            <h3 style="margin-top: 1.5rem;">2. Payment Details</h3>
            <div class="form-group">
                <label for="cardNumber">Card Number</label>
                <input type="text" id="cardNumber" name="card" placeholder="4532 •••• •••• 8910" required />
            </div>

            <button type="submit" id="btnPlaceOrder" class="btn btn-success" style="width: 100%; padding: 14px; font-size: 1.1rem; margin-top: 2rem;">Place Order</button>
        </form>
    </div>
</div>
</body></html>"""

V1_ORDER_SUCCESS_HTML = f"""<!DOCTYPE html>
<html>
<head><title>Order Confirmed - MoonStore V1</title>{V1_STYLES}</head>
<body>
{V1_NAVBAR}
<div class="container" style="max-width: 500px; text-align: center;">
    <div class="card" style="padding: 3rem 2rem;">
        <div style="font-size: 3rem; color: #16a34a; margin-bottom: 1rem;">✓</div>
        <h2 id="confirmationHeading">Order Confirmed!</h2>
        <p style="color: #64748b;">Your order #MS-94821 has been successfully placed.</p>
        <div style="margin-top: 2rem;">
            <a href="/ecommerce/v1/products" id="btnContinueShopping" class="btn btn-primary">Return to Catalog</a>
        </div>
    </div>
</div>
</body></html>"""


# =============================================================================
# VERSION 2 (REFACTORED / MUTATED) HTML TEMPLATES
# =============================================================================

V2_NAVBAR = """
<!-- V2 Header: Changed tag hierarchy, modernized styling, renamed IDs -->
<header id="appHeaderV2" class="bg-slate-900 border-b border-slate-800">
    <nav class="max-w-6xl mx-auto flex items-center justify-between px-6 py-4">
        <div class="flex items-center space-x-3">
            <a href="/ecommerce/v2/products" id="brandLogoV2" class="text-xl font-bold tracking-tight text-white hover:text-amber-400">MoonStore Labs</a>
            <span class="text-xs bg-amber-500/20 text-amber-400 px-2 py-0.5 rounded font-mono">v2.0</span>
        </div>
        <div class="flex items-center space-x-2">
            <input type="search" id="catalogSearchQuery" placeholder="Search catalog..." class="bg-slate-800 text-white border border-slate-700 rounded-md px-3 py-1.5 text-sm" />
            <button type="button" id="btnExecuteSearch" class="bg-blue-600 hover:bg-blue-700 text-white text-sm px-3 py-1.5 rounded-md font-medium">Find</button>
        </div>
        <div class="flex items-center space-x-6 text-sm font-medium">
            <a href="/ecommerce/v2/products" class="text-slate-300 hover:text-white">Storefront</a>
            <a href="/ecommerce/v2/cart" id="userCartSummary" class="text-slate-300 hover:text-white flex items-center">
                <span>Bag</span>
                <span class="ml-1.5 bg-blue-600 text-white text-xs px-2 py-0.5 rounded-full font-bold">2</span>
            </a>
            <a href="/ecommerce/v2/login" id="linkUserAccount" class="text-slate-300 hover:text-white">Sign In</a>
        </div>
    </nav>
</header>
"""

V2_STYLES = """
<style>
    * { box-sizing: border-box; font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    body { margin: 0; background: #0f1013; color: #f2efe8; }
    .max-w-6xl { max-width: 1150px; margin: 0 auto; }
    .container-v2 { max-width: 1050px; margin: 2.5rem auto; padding: 0 1.5rem; }
    .card-v2 { background: #17191e; border: 1px solid #2a2d35; border-radius: 12px; padding: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.4); margin-bottom: 2rem; }
    .form-field-v2 { margin-bottom: 1.25rem; }
    .form-field-v2 label { display: block; margin-bottom: 0.5rem; font-size: 0.9rem; font-weight: 500; color: #8b9099; }
    .form-field-v2 input { width: 100%; padding: 10px 14px; background: #22262f; border: 1px solid #363b47; border-radius: 8px; color: #f2efe8; font-size: 0.95rem; }
    .btn-action-primary { display: inline-block; background: #e0a45c; color: #0f1013; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: none; cursor: pointer; text-align: center; text-decoration: none; transition: all 0.2s; }
    .btn-action-primary:hover { background: #f0b56e; transform: translateY(-1px); }
    .btn-action-secondary { background: #2a2d35; color: #f2efe8; font-weight: 600; padding: 10px 16px; border-radius: 8px; border: 1px solid #363b47; cursor: pointer; }
    .product-grid-v2 { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 2rem; }
    .product-tile { background: #17191e; border: 1px solid #2a2d35; border-radius: 12px; padding: 1.5rem; display: flex; flex-direction: column; justify-content: space-between; }
    .product-tile:hover { border-color: #e0a45c; }
    .tile-price { font-size: 1.35rem; font-weight: 800; color: #e0a45c; margin: 0.75rem 0; }
    .cart-summary-table { width: 100%; border-collapse: collapse; margin-bottom: 2rem; }
    .cart-summary-table th { padding: 14px; text-align: left; border-bottom: 1px solid #2a2d35; color: #8b9099; font-size: 0.85rem; text-transform: uppercase; }
    .cart-summary-table td { padding: 16px 14px; border-bottom: 1px solid #22262f; }
</style>
"""

V2_LOGIN_HTML = f"""<!DOCTYPE html>
<html>
<head><title>Sign In - MoonStore V2</title>{V2_STYLES}</head>
<body>
{V2_NAVBAR}
<div class="container-v2" style="max-width: 440px;">
    <div class="card-v2">
        <h2 style="margin-top: 0;">Portal Sign In</h2>
        <p style="color: #8b9099; font-size: 0.9rem; margin-bottom: 1.5rem;">Secure authentication via Moon Sanctum Labs identity.</p>
        
        <!-- V2 Mutations:
             - Form has ID authContainerForm
             - Button ID changed from #btnLogin to #btnSignInSubmit
             - Button class changed to .btn-action-primary
             - Button text changed from 'Login' to 'Sign In' (Semantic synonym)
        -->
        <form action="/ecommerce/v2/products" method="GET" id="authContainerForm">
            <div class="form-field-v2">
                <label for="userEmailInput">Account Email</label>
                <input type="text" id="userEmailInput" name="username" placeholder="name@moonsanctum.com" data-testid="auth-user" required />
            </div>
            <div class="form-field-v2">
                <label for="userSecretKey">Security Password</label>
                <input type="password" id="userSecretKey" name="password" placeholder="••••••••••••" data-testid="auth-pass" required />
            </div>
            <button type="submit" id="btnSignInSubmit" class="btn-action-primary" style="width: 100%; margin-top: 1.5rem;">Sign In</button>
        </form>
    </div>
</div>
</body></html>"""

V2_REGISTER_HTML = f"""<!DOCTYPE html>
<html>
<head><title>Register - MoonStore V2</title>{V2_STYLES}</head>
<body>
{V2_NAVBAR}
<div class="container-v2" style="max-width: 480px;">
    <div class="card-v2">
        <h2>Join Community</h2>
        <!-- V2 Mutations:
             - Button ID changed from #btnRegisterSubmit to #btnCreateAccount
             - Text changed from 'Register' to 'Create Account'
        -->
        <form action="/ecommerce/v2/products" method="GET" id="createProfileForm">
            <div class="form-field-v2">
                <label for="memberName">Member Name</label>
                <input type="text" id="memberName" name="fullName" placeholder="Jane Doe" required />
            </div>
            <div class="form-field-v2">
                <label for="memberEmail">Email Address</label>
                <input type="email" id="memberEmail" name="email" placeholder="jane@example.com" required />
            </div>
            <div class="form-field-v2">
                <label for="memberPassword">Password</label>
                <input type="password" id="memberPassword" name="password" placeholder="Min 8 characters" required />
            </div>
            <button type="submit" id="btnCreateAccount" class="btn-action-primary" style="width: 100%;">Create Account</button>
        </form>
    </div>
</div>
</body></html>"""

V2_PRODUCTS_HTML = f"""<!DOCTYPE html>
<html>
<head><title>Storefront - MoonStore V2</title>{V2_STYLES}</head>
<body>
{V2_NAVBAR}
<div class="container-v2">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <h2>Curated Hardware</h2>
        <span style="background: #22262f; color: #8b9099; padding: 4px 12px; border-radius: 9999px; font-size: 0.85rem;">3 Products Available</span>
    </div>

    <!-- V2 Mutations:
         - Buttons changed from 'Add to Cart' to 'Add to Bag'
         - IDs renamed with kebab-case: #btnAddToCart1 -> #btn-add-bag-101
         - Wrapped inside action container div
    -->
    <div class="product-grid-v2">
        <div class="product-tile" id="tile_101">
            <div>
                <h3>Quantum Mechanical Keyboard</h3>
                <p style="color: #8b9099; font-size: 0.9rem;">Ultra-responsive tactile optical switches with per-key RGB.</p>
                <div class="tile-price">$149.99</div>
            </div>
            <div class="tile-actions" style="margin-top: 1.25rem;">
                <button type="button" id="btn-add-bag-101" class="btn-action-primary" aria-label="Add Quantum Mechanical Keyboard to Bag" style="width: 100%;" onclick="window.location='/ecommerce/v2/cart'">Add to Bag</button>
            </div>
        </div>
        <div class="product-tile" id="tile_102">
            <div>
                <h3>Ergonomic Precision Mouse</h3>
                <p style="color: #8b9099; font-size: 0.9rem;">Wireless ultra-low latency 26K DPI optical sensor.</p>
                <div class="tile-price">$89.99</div>
            </div>
            <div class="tile-actions" style="margin-top: 1.25rem;">
                <button type="button" id="btn-add-bag-102" class="btn-action-primary" aria-label="Add Ergonomic Precision Mouse to Bag" style="width: 100%;" onclick="window.location='/ecommerce/v2/cart'">Add to Bag</button>
            </div>
        </div>
        <div class="product-tile" id="tile_103">
            <div>
                <h3>Noise-Cancelling Studio Headset</h3>
                <p style="color: #8b9099; font-size: 0.9rem;">Studio reference planar acoustic transducers.</p>
                <div class="tile-price">$249.99</div>
            </div>
            <div class="tile-actions" style="margin-top: 1.25rem;">
                <button type="button" id="btn-add-bag-103" class="btn-action-primary" aria-label="Add Noise-Cancelling Studio Headset to Bag" style="width: 100%;" onclick="window.location='/ecommerce/v2/cart'">Add to Bag</button>
            </div>
        </div>
    </div>
</div>
</body></html>"""

V2_CART_HTML = f"""<!DOCTYPE html>
<html>
<head><title>Bag - MoonStore V2</title>{V2_STYLES}</head>
<body>
{V2_NAVBAR}
<div class="container-v2">
    <div class="card-v2">
        <h2 style="margin-top: 0;">Order Summary</h2>
        <table class="cart-summary-table">
            <thead>
                <tr><th>Hardware</th><th>Quantity</th><th>Unit Price</th><th>Subtotal</th></tr>
            </thead>
            <tbody>
                <tr><td>Quantum Mechanical Keyboard</td><td>1</td><td>$149.99</td><td>$149.99</td></tr>
                <tr><td>Ergonomic Precision Mouse</td><td>1</td><td>$89.99</td><td>$89.99</td></tr>
            </tbody>
        </table>

        <!-- V2 Mutations:
             - Button renamed from #btnProceedCheckout to #btn-checkout-step
             - Text changed from 'Proceed to Checkout' to 'Continue to Payment'
             - Reordered into sticky right-aligned summary card
        -->
        <div style="display: flex; justify-content: space-between; align-items: center; background: #22262f; padding: 1.5rem; border-radius: 8px;">
            <div style="font-size: 1.3rem; font-weight: 800; color: #f2efe8;">
                Total Due: <span style="color: #e0a45c;">$239.98</span>
            </div>
            <div>
                <a href="/ecommerce/v2/checkout" id="btn-checkout-step" class="btn-action-primary" style="font-size: 1.1rem; padding: 14px 28px;">Continue to Payment</a>
            </div>
        </div>
    </div>
</div>
</body></html>"""

V2_CHECKOUT_HTML = f"""<!DOCTYPE html>
<html>
<head><title>Checkout - MoonStore V2</title>{V2_STYLES}</head>
<body>
{V2_NAVBAR}
<div class="container-v2" style="max-width: 720px;">
    <div class="card-v2">
        <h2 style="margin-top: 0;">Finalize Transaction</h2>
        <form action="/ecommerce/v2/order-success" method="GET" id="paymentProcessForm">
            <fieldset style="border: 1px solid #2a2d35; border-radius: 8px; padding: 1.25rem; margin-bottom: 1.5rem;">
                <legend style="color: #e0a45c; font-weight: 600; padding: 0 8px;">Delivery Destination</legend>
                <div class="form-field-v2">
                    <label for="destAddress">Street Address</label>
                    <input type="text" id="destAddress" name="address" placeholder="123 Tech Boulevard" required />
                </div>
                <div class="form-field-v2">
                    <label for="destCity">Destination City</label>
                    <input type="text" id="destCity" name="city" placeholder="Kolkata" required />
                </div>
            </fieldset>

            <fieldset style="border: 1px solid #2a2d35; border-radius: 8px; padding: 1.25rem; margin-bottom: 2rem;">
                <legend style="color: #e0a45c; font-weight: 600; padding: 0 8px;">Payment Authorization</legend>
                <div class="form-field-v2">
                    <label for="cardAccount">Card Number</label>
                    <input type="text" id="cardAccount" name="card" placeholder="4532 •••• •••• 8910" required />
                </div>
            </fieldset>

            <!-- V2 Mutations:
                 - Button ID changed from #btnPlaceOrder to #btnCompletePurchase
                 - Text changed from 'Place Order' to 'Complete Purchase'
                 - Styled with brand copper button
            -->
            <button type="submit" id="btnCompletePurchase" class="btn-action-primary" style="width: 100%; font-size: 1.15rem; padding: 14px;">Complete Purchase</button>
        </form>
    </div>
</div>
</body></html>"""

V2_ORDER_SUCCESS_HTML = f"""<!DOCTYPE html>
<html>
<head><title>Confirmed - MoonStore V2</title>{V2_STYLES}</head>
<body>
{V2_NAVBAR}
<div class="container-v2" style="max-width: 520px; text-align: center;">
    <div class="card-v2" style="padding: 3.5rem 2rem;">
        <div style="font-size: 3.5rem; color: #e0a45c; margin-bottom: 1rem;">✓</div>
        <h2 id="confirmationNotice">Transaction Complete</h2>
        <p style="color: #8b9099;">Your hardware consignment #MS-94821 is being prepared.</p>
        <div style="margin-top: 2.5rem;">
            <a href="/ecommerce/v2/products" id="btnBackToStorefront" class="btn-action-secondary">Back to Storefront</a>
        </div>
    </div>
</div>
</body></html>"""

# =============================================================================
# AMBIGUOUS NEAR-TIE DEMO PAGE (For Negative Rejection Demonstration)
# =============================================================================

AMBIGUOUS_DEMO_HTML = f"""<!DOCTYPE html>
<html>
<head><title>Ambiguity & Actionability Diagnostics</title>{V2_STYLES}</head>
<body>
{V2_NAVBAR}
<div class="container-v2" style="max-width: 600px;">
    <div class="card-v2">
        <h2>Ambiguity Protection Diagnostic</h2>
        <p style="color: #8b9099;">This page contains intentional near-tie candidates with identical text and hierarchy. The self-healing engine must detect that score difference < 0.10 and abstain safely.</p>
        
        <div style="border: 1px dashed #363b47; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <h3>Payment Method Selection (Ambiguous Near-Ties)</h3>
            <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                <button type="button" class="btn-action-primary payment-select-btn" id="payMethodOption1" style="flex: 1;">Select Option</button>
                <button type="button" class="btn-action-primary payment-select-btn" id="payMethodOption2" style="flex: 1;">Select Option</button>
            </div>
        </div>

        <div style="border: 1px dashed #363b47; padding: 1.5rem; border-radius: 8px;">
            <h3>Actionability Failure (Disabled Target)</h3>
            <p style="color: #8b9099; font-size: 0.9rem;">Requires accepting terms before activation.</p>
            <button type="button" class="btn-action-primary" id="btnDisabledCheckout" disabled style="opacity: 0.4; cursor: not-allowed; width: 100%;">Express Checkout (Locked)</button>
        </div>
    </div>
</div>
</body></html>"""


def get_ecommerce_page(path: str) -> str | None:
    """
    Router for the demonstration e-commerce store.
    """
    clean_path = path.rstrip("/").split("?")[0]

    # V1 Routes
    if clean_path in ("/ecommerce", "/ecommerce/v1", "/ecommerce/v1/products"):
        return V1_PRODUCTS_HTML
    elif clean_path == "/ecommerce/v1/login":
        return V1_LOGIN_HTML
    elif clean_path == "/ecommerce/v1/register":
        return V1_REGISTER_HTML
    elif clean_path == "/ecommerce/v1/cart":
        return V1_CART_HTML
    elif clean_path == "/ecommerce/v1/checkout":
        return V1_CHECKOUT_HTML
    elif clean_path == "/ecommerce/v1/order-success":
        return V1_ORDER_SUCCESS_HTML

    # V2 Routes
    elif clean_path in ("/ecommerce/v2", "/ecommerce/v2/products"):
        return V2_PRODUCTS_HTML
    elif clean_path == "/ecommerce/v2/login":
        return V2_LOGIN_HTML
    elif clean_path == "/ecommerce/v2/register":
        return V2_REGISTER_HTML
    elif clean_path == "/ecommerce/v2/cart":
        return V2_CART_HTML
    elif clean_path == "/ecommerce/v2/checkout":
        return V2_CHECKOUT_HTML
    elif clean_path == "/ecommerce/v2/order-success":
        return V2_ORDER_SUCCESS_HTML

    # Diagnostic / Ambiguous Rejection Route
    elif clean_path in ("/ecommerce/ambiguous", "/ecommerce/v1/ambiguous", "/ecommerce/v2/ambiguous"):
        return AMBIGUOUS_DEMO_HTML

    return None
