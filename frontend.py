import streamlit as st
import requests
import json
import csv
from io import StringIO

# Backend API URL - Update if deployed elsewhere
API_BASE = "https://stableflow-backend.onrender.com"# Change to your Render URL, e.g., "https://your-mvp.onrender.com"

st.set_page_config(
    page_title="StableFlow Pay - Secure Stablecoin Movement",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS theme with PROPER font scaling
st.markdown("""
    <style>
    /* Main theme colors - professional blue/gray palette */
    :root {
        --primary-blue: #1f3d7a;
        --secondary-blue: #2c5282;
        --accent-blue: #3182ce;
        --dark-gray: #2d3748;
        --medium-gray: #4a5568;
        --light-gray: #edf2f7;
        --white: #ffffff;
        --success: #38a169;
        --warning: #d69e2e;
        --error: #e53e3e;
    }
    /* Base font scaling - target specific elements */
    .main .block-container {
        font-size: 24px;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .main-header {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        color: var(--primary-blue);
        margin: 1rem 0 2rem 0;
        text-align: center;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        background: linear-gradient(135deg, var(--primary-blue), var(--accent-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        padding: 1rem 0;
    }
    .section-header {
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        color: var(--dark-gray);
        margin: 2rem 0 1.5rem 0;
        border-bottom: 2px solid var(--light-gray);
        padding-bottom: 1rem;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    .subsection-header {
        font-size: 2.4rem !important;
        font-weight: 600 !important;
        color: var(--secondary-blue);
        margin: 1.5rem 0 1rem 0;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    /* Feature cards */
    .feature-card {
        background: var(--white);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid var(--accent-blue);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #e2e8f0;
        height: 100%;
    }
    .feature-card-title {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        color: var(--primary-blue);
    }
    .feature-card-content {
        font-size: 1.3rem !important;
        line-height: 1.6 !important;
        margin: 0 !important;
    }
    .form-section {
        background: var(--white);
        border-radius: 12px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 2px solid #e2e8f0;
    }
    .success-box {
        background: #f0fff4;
        border: 2px solid #9ae6b4;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-size: 1.3rem;
    }
    .info-box {
        background: #ebf8ff;
        border: 2px solid #90cdf4;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-size: 1.3rem;
    }
    .warning-box {
        background: #fffaf0;
        border: 2px solid #faf089;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-size: 1.3rem;
    }
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 1rem 2rem;
        font-weight: 600;
        font-size: 1.5rem !important;
        transition: all 0.2s ease;
        height: auto;
        min-height: 70px;
    }
    /* Form elements */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 1rem;
        font-size: 1.3rem !important;
    }
    /* Dropdown fixes */
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 1rem !important;
        font-size: 1.3rem !important;
        height: auto !important;
        min-height: 65px !important;
    }
    /* Labels */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stTextArea label,
    .stSlider label {
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        color: var(--dark-gray) !important;
        margin-bottom: 0.5rem !important;
    }
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        color: var(--medium-gray);
        font-size: 1.2rem !important;
        border-top: 2px solid #e2e8f0;
    }
    /* Remove empty space */
    .element-container {
        margin-bottom: 0.5rem;
    }
 
    /* Better spacing for form elements */
    .stForm {
        margin-bottom: 1rem;
    }
    /* Large metric font for storage summary */
    .large-metric .stMetric {
        font-size: 1.6rem !important;
    }
 
    .large-metric .stMetric label {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }
 
    .large-metric .stMetric div {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
    }
    /* Create Wallet specific larger fonts */
    .create-wallet-form {
        font-size: 1.4rem !important;
    }
 
    .create-wallet-form .stSelectbox label,
    .create-wallet-form .stNumberInput label,
    .create-wallet-form .stTextInput label {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }
    /* Specific styling for Create Wallet form labels */
    .create-wallet-labels .stSelectbox label,
    .create-wallet-labels .stNumberInput label,
    .create-wallet-labels .stTextInput label {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--primary-blue) !important;
        margin-bottom: 0.8rem !important;
    }
 
    .create-wallet-labels .stSelectbox > div > div > select,
    .create-wallet-labels .stNumberInput > div > div > input,
    .create-wallet-labels .stTextInput > div > div > input {
        font-size: 1.6rem !important;
        padding: 1.2rem !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'wallet_result' not in st.session_state:
    st.session_state.wallet_result = None
if 'shard_assignments' not in st.session_state:
    st.session_state.shard_assignments = None
if 'shard_tiers' not in st.session_state:
    st.session_state.shard_tiers = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'value_thresholds' not in st.session_state:
    st.session_state.value_thresholds = {
        "low": 2.0,
        "mid": 5.0, 
        "high": 10.0
    }

# Storage options dropdown values
STORAGE_OPTIONS = ["Keychain", "AWS", "Azure", "Google Cloud", "Proton Drive", "pCloud"]

# Tier options for manual assignment
TIER_OPTIONS = ["tier1", "tier2", "tier3"]

# Define page order for navigation
PAGE_ORDER = [
    "Home",
    "Create Wallet",
    "Shard Storage Assignment",
    "Transaction Value Thresholds",
    "Reconstruct Key",
    "Sign Transaction",
    "Authorize Queued Tx",
    "Pending Transactions",
    "Wallets"
]

# Professional sidebar navigation
with st.sidebar:
    st.markdown("## Navigation")
    for page_name in PAGE_ORDER:
        if st.button(page_name, use_container_width=True, key=f"nav_{page_name}"):
            st.session_state.current_page = page_name
            st.rerun()
    st.markdown("---")
    st.markdown("### System Status")
    # System metrics
    try:
        response = requests.get(f"{API_BASE}/wallets")
        wallet_count = response.json().get("count", 0) if response.status_code == 200 else 0
    except:
        wallet_count = 0
    
    try:
        response = requests.get(f"{API_BASE}/transactions/pending")
        pending_count = response.json().get("count", 0) if response.status_code == 200 else 0
    except:
        pending_count = 0
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Wallets", wallet_count)
    with col2:
        st.metric("Pending TX", pending_count)
    st.markdown("---")
    if st.button("Reset Session", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.current_page = "Home"
        st.rerun()

def render_navigation_buttons():
    """Render Next and Back buttons for page navigation"""
    current_index = PAGE_ORDER.index(st.session_state.current_page)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if current_index > 0:
            prev_page = PAGE_ORDER[current_index - 1]
            if st.button("Back", use_container_width=True, key="back_button"):
                st.session_state.current_page = prev_page
                st.rerun()
    with col3:
        if current_index < len(PAGE_ORDER) - 1:
            next_page = PAGE_ORDER[current_index + 1]
            if st.button("Next", use_container_width=True, key="next_button"):
                st.session_state.current_page = next_page
                st.rerun()

# Page routing
current_page = st.session_state.current_page

if current_page == "Home":
    st.markdown('<h1 class="main-header">StableFlow Pay - Secure Stablecoin Movement</h1>', unsafe_allow_html=True)
 
    # Feature cards with bullet points
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-card-title">Secure Sharding</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card-content">
        • Split private keys across multiple devices<br>
        • Progressive escalation for Boosted Auths<br>
        • Cross-device reconstruction<br>
        • No single point of failure
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-card-title">Multi-Signature</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card-content">
        • Threshold-based authorization<br>
        • Real Mainnet integration (currently implemented only for Solana)<br>
        • Stablecoins : USDT, USDC, PYUSD & USDe<br>
        • High-value transaction queuing
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
    with col3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-card-title">Smart Escalation</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card-content">
        • Value-based security tiers<br>
        • Fraud Resistance by Design<br>
        • Automatic authorization levels<br>
        • Cross-cloud backup & recovery
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    # Quick actions
    st.markdown('<h2 class="section-header">Quick Actions</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Create New Wallet", use_container_width=True):
            st.session_state.current_page = "Create Wallet"
            st.rerun()
    with col2:
        if st.button("Send Transaction", use_container_width=True):
            st.session_state.current_page = "Sign Transaction"
            st.rerun()
    with col3:
        if st.button("View Pending", use_container_width=True):
            st.session_state.current_page = "Pending Transactions"
            st.rerun()
    # Navigation buttons
    render_navigation_buttons()

elif current_page == "Create Wallet":
    st.markdown('<h1 class="main-header">Create Secure Wallet</h1>', unsafe_allow_html=True)
    st.markdown('<div class="create-wallet-labels">', unsafe_allow_html=True)
 
    with st.container():
        with st.form("create_wallet_form"):
            col1, col2 = st.columns(2)
        
            with col1:
                # Blockchain network dropdown
                blockchain_network = st.selectbox(
                    "Select Chain or Network:",
                    ["Solana", "Ethereum", "Aave", "Base", "Sui", "BSC", "Tron", "Arbitrum"],
                    help="Select the blockchain network for this wallet"
                )
             
                scheme = st.selectbox("Scheme", ["full", "spep"],
                                    help="Sharing scheme: full or spep (Staged Priority Escalation Protocol)")
               
                # SIMPLIFIED CONFIGURATION - NO STORAGE SETS
                threshold = st.number_input("Reconstruction Threshold", min_value=2, value=2,
                                          help="Minimum shards required to reconstruct private key")
                total_shards = st.number_input("Total Shards", min_value=threshold, value=6,
                                             help="Total number of shards to generate")
        
            with col2:
                # For SPEP scheme, show groups configuration
                if scheme == "spep":
                    num_groups = st.number_input("Number of Groups", min_value=1, max_value=total_shards, value=3,
                                               help="Number of groups for SPEP scheme distribution")
                else:
                    num_groups = 1
                
                # Show basic configuration summary
                st.markdown("**Configuration Summary**")
                st.info(f"""
                **Total Shards**: {total_shards}
                **Threshold**: {threshold}
                **Scheme**: {scheme}
                """)
        
            submitted = st.form_submit_button("Create Wallet", use_container_width=True)
        
            if submitted:
                # Prepare data for API - basic scheme configuration only
                data = {
                    "threshold": threshold,
                    "shares": total_shards,
                    "scheme": scheme,
                    "num_groups": num_groups
                }
                   
                try:
                    response = requests.post(f"{API_BASE}/wallets/create", json=data)
                    if response.status_code == 200:
                        st.session_state.wallet_result = response.json()
                        st.success("Wallet created successfully!")
                       
                        # Display wallet information INCLUDING SHARDS
                        result = st.session_state.wallet_result
                        st.markdown("### Wallet Created Successfully!")
                        st.info(f"**Wallet ID:** {result['wallet_id']}")
                        st.info(f"**Public Key:** {result['pubkey']}")
                        st.info(f"**Total Shards:** {len(result.get('shards', []))}")
                       
                        # DISPLAY THE ACTUAL SHARDS
                        st.markdown("### Generated Shards")
                        st.warning("**Important:** Save these shards securely. They are required for wallet reconstruction.")
                        
                        for i, shard in enumerate(result.get('shards', [])):
                            st.text_input(f"Shard {i+1}", value=shard, key=f"shard_{i}", disabled=True)
                       
                        # Initialize manual assignments for next page
                        st.session_state.shard_assignments = {shard: STORAGE_OPTIONS[0] for shard in result.get('shards', [])}
                        st.session_state.shard_tiers = {shard: TIER_OPTIONS[0] for shard in result.get('shards', [])}
                    else:
                        st.error(f"Error: {response.json().get('detail')}")
                except Exception as e:
                    st.error(f"Failed to create wallet: {str(e)}")
 
    st.markdown('</div>', unsafe_allow_html=True)
    # Navigation buttons
    render_navigation_buttons()

elif current_page == "Shard Storage Assignment":
    st.markdown('<h1 class="main-header">Shard Storage Assignment</h1>', unsafe_allow_html=True)
 
    if not st.session_state.wallet_result:
        st.warning("Please create a wallet first before assigning shard storage.")
        if st.button("Go to Create Wallet"):
            st.session_state.current_page = "Create Wallet"
            st.rerun()
    else:
        shards = st.session_state.wallet_result.get('shards', [])
    
        st.markdown(f'<div class="subsection-header">Assigning {len(shards)} Shards to Storage Locations and Tiers</div>', unsafe_allow_html=True)
        st.info("""
        **Manual Assignment Required:** 
        - Assign each shard to a storage location
        - Assign each shard a security tier
        - Tiers determine authorization level required for transactions
        """)
    
        # Manual assignment for storage and tiers
        cols = st.columns(2)
        for i, shard in enumerate(shards):
            with cols[i % 2]:
                st.markdown(f"**Shard {i+1}:** `{shard}`")
                
                # Storage assignment
                st.session_state.shard_assignments[shard] = st.selectbox(
                    f"Storage for Shard {i+1}",
                    STORAGE_OPTIONS,
                    index=STORAGE_OPTIONS.index(st.session_state.shard_assignments.get(shard, STORAGE_OPTIONS[0])),
                    key=f"storage_shard_{i}"
                )
                
                # Tier assignment (MANUAL - NO AUTOMATIC ASSIGNMENT)
                st.session_state.shard_tiers[shard] = st.selectbox(
                    f"Tier for Shard {i+1}",
                    TIER_OPTIONS,
                    index=TIER_OPTIONS.index(st.session_state.shard_tiers.get(shard, TIER_OPTIONS[0])),
                    key=f"tier_shard_{i}"
                )
                st.markdown("---")
    
        # Storage/tier summary
        st.markdown("### Assignment Summary")
        storage_counts = {}
        tier_counts = {}
        for storage in st.session_state.shard_assignments.values():
            storage_counts[storage] = storage_counts.get(storage, 0) + 1
        for tier in st.session_state.shard_tiers.values():
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
    
        # Display storage
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Storage Distribution:**")
            for storage, count in storage_counts.items():
                st.write(f"- {storage}: {count} shards")
        
        # Display tiers
        with col2:
            st.markdown("**Tier Distribution:**")
            for tier, count in tier_counts.items():
                st.write(f"- {tier}: {count} shards")
    
        # Download options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Download Shard Assignments", use_container_width=True):
                output = StringIO()
                writer = csv.writer(output)
                writer.writerow(["Shard", "Assigned Storage", "Assigned Tier", "Security Level"])
                for shard in shards:
                    storage = st.session_state.shard_assignments.get(shard, "Unassigned")
                    tier = st.session_state.shard_tiers.get(shard, "Unassigned")
                    level = "High" if storage in ["AWS", "Azure", "Google Cloud", "Proton Drive", "pCloud"] else "Medium"
                    writer.writerow([shard, storage, tier, level])
                st.download_button(
                    "Download CSV",
                    output.getvalue(),
                    "shard_assignments.csv",
                    "text/csv",
                    use_container_width=True
                )
    
        with col2:
            st.download_button(
                "Download Wallet Details",
                data=json.dumps(st.session_state.wallet_result, indent=2),
                file_name="wallet_details.json",
                use_container_width=True
            )
    
        st.success("Shard storage and tier assignments completed. Proceed to set transaction value thresholds.")
    # Navigation buttons
    render_navigation_buttons()

elif current_page == "Transaction Value Thresholds":
    st.markdown('<h1 class="main-header">Transaction Value Thresholds</h1>', unsafe_allow_html=True)
 
    if not st.session_state.wallet_result:
        st.warning("Please create a wallet and assign shards first before setting value thresholds.")
        if st.button("Go to Create Wallet"):
            st.session_state.current_page = "Create Wallet"
            st.rerun()
    else:
        wallet_id = st.session_state.wallet_result.get('wallet_id')
        
        st.markdown('<div class="subsection-header">Set Custom Transaction Value Thresholds</div>', unsafe_allow_html=True)
        st.info("""
        Configure the dollar value thresholds that determine when transactions require additional authorization:
        - **Low Value**: Direct signing (no queue)
        - **Mid Value**: Requires tier2 authorization (queued)  
        - **High Value**: Requires tier3 authorization (queued)
        - **Above High**: Transactions rejected
        """)
        
        with st.form("value_thresholds_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                low_threshold = st.number_input(
                    "Low Value Threshold ($)",
                    min_value=0.01,
                    max_value=100.0,
                    value=st.session_state.value_thresholds["low"],
                    step=0.1,
                    help="Transactions ≤ this value use tier1 (direct signing)"
                )
            
            with col2:
                mid_threshold = st.number_input(
                    "Mid Value Threshold ($)",
                    min_value=0.02,
                    max_value=100.0,
                    value=st.session_state.value_thresholds["mid"],
                    step=0.1,
                    help="Transactions between low and mid use tier2 (queued)"
                )
            
            with col3:
                high_threshold = st.number_input(
                    "High Value Threshold ($)",
                    min_value=0.03,
                    max_value=100.0,
                    value=st.session_state.value_thresholds["high"],
                    step=0.1,
                    help="Transactions between mid and high use tier3 (queued)"
                )
            
            # Validation
            if low_threshold >= mid_threshold:
                st.error("Low threshold must be less than Mid threshold")
            elif mid_threshold >= high_threshold:
                st.error("Mid threshold must be less than High threshold")
            else:
                st.session_state.value_thresholds = {
                    "low": low_threshold,
                    "mid": mid_threshold,
                    "high": high_threshold
                }
            
            submitted = st.form_submit_button("Save Value Thresholds", use_container_width=True)
            
            if submitted and low_threshold < mid_threshold < high_threshold:
                try:
                    data = {
                        "wallet_id": wallet_id,
                        "low_threshold": low_threshold,
                        "mid_threshold": mid_threshold,
                        "high_threshold": high_threshold
                    }
                    
                    response = requests.post(f"{API_BASE}/wallets/set-value-thresholds", json=data)
                    if response.status_code == 200:
                        st.success("Value thresholds saved successfully!")
                        
                        # Display current configuration
                        st.markdown("### Current Threshold Configuration")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Low Value", f"${low_threshold}", "Tier1 - Direct")
                        with col2:
                            st.metric("Mid Value", f"${mid_threshold}", "Tier2 - Queued")
                        with col3:
                            st.metric("High Value", f"${high_threshold}", "Tier3 - Queued")
                        with col4:
                            st.metric("Above High", "Rejected", "Not Allowed")
                            
                    else:
                        st.error(f"Error: {response.json().get('detail')}")
                except Exception as e:
                    st.error(f"Failed to save value thresholds: {str(e)}")
        
        # Show current thresholds from backend
        try:
            response = requests.get(f"{API_BASE}/wallets/{wallet_id}/value-thresholds")
            if response.status_code == 200:
                thresholds_data = response.json()
                st.markdown("### Current Backend Thresholds")
                st.json(thresholds_data)
        except Exception as e:
            st.warning("Could not fetch current thresholds from backend")
    
    # Navigation buttons
    render_navigation_buttons()

elif current_page == "Reconstruct Key":
    st.markdown('<h1 class="main-header">Reconstruct Private Key</h1>', unsafe_allow_html=True)
    with st.container():
        with st.form("reconstruct_form"):
            st.markdown('<div class="subsection-header">Enter Shard Information</div>', unsafe_allow_html=True)
        
            wallet_id = st.text_input("Wallet ID", placeholder="Enter your wallet identifier")
            shards_input = st.text_area("Shards (one per line)",
                                      placeholder="Paste your shards here, one per line",
                                      height=200)
            level = st.selectbox("Security Level", ["tier1", "tier2", "tier3"],
                               help="Required security level for reconstruction (tier1 = highest priority)")
        
            submitted = st.form_submit_button("Reconstruct Private Key", use_container_width=True)
        
            if submitted:
                shards = [s.strip() for s in shards_input.split("\n") if s.strip()]
                if not wallet_id or not shards:
                    st.error("Please provide both Wallet ID and shards")
                else:
                    data = {
                        "wallet_id": wallet_id,
                        "shards": shards,
                        "level": level
                    }
                    try:
                        with st.spinner("Reconstructing private key from shards..."):
                            response = requests.post(f"{API_BASE}/wallets/reconstruct", json=data)
                            if response.status_code == 200:
                                result = response.json()
                                st.success("Private key reconstructed successfully!")
                                st.json(result)
                                st.warning("Private key reconstructed - handle with extreme security!")
                            else:
                                st.error(f"Error: {response.json().get('detail')}")
                    except Exception as e:
                        st.error(f"Failed to reconstruct: {str(e)}")
    # Navigation buttons
    render_navigation_buttons()

elif current_page == "Sign Transaction":
    st.markdown('<h1 class="main-header">Sign Transaction</h1>', unsafe_allow_html=True)
    with st.container():
        with st.form("sign_tx_form"):
            st.markdown('<div class="subsection-header">Transaction Details</div>', unsafe_allow_html=True)
        
            col1, col2 = st.columns(2)
            with col1:
                wallet_id = st.text_input("Wallet ID")
                to_address = st.text_input("To Address", placeholder="Recipient blockchain address")
                amount = st.number_input("Amount", min_value=0.0001, value=1.0, step=0.1)
        
            with col2:
                token_symbol = st.selectbox("Token", [None, "USDT", "USDC", "PYUSD", "USDe"])
                shards_input = st.text_area("Shards (one per line)", height=150)
                level = st.selectbox("Security Level", ["tier1", "tier2", "tier3"],
                                     help="Required security level (tier1 = highest priority)")
        
            submitted = st.form_submit_button("Sign & Send Transaction", use_container_width=True)
        
            if submitted:
                shards = [s.strip() for s in shards_input.split("\n") if s.strip()]
                data = {
                    "wallet_id": wallet_id,
                    "to_address": to_address,
                    "amount": amount,
                    "token_symbol": token_symbol,
                    "shards": shards,
                    "level": level
                }
                try:
                    with st.spinner("Processing transaction with security escalation..."):
                        response = requests.post(f"{API_BASE}/transactions/sign", json=data)
                        if response.status_code == 200:
                            result = response.json()
                            if result.get("status") == "queued":
                                st.warning("🚨 Transaction queued for enhanced security authorization")
                            elif result.get("status") == "rejected":
                                st.error(f"❌ Transaction rejected: {result.get('message')}")
                            else:
                                st.success("✅ Transaction signed and broadcasted successfully!")
                                txid = result.get('txid')
                                if txid:
                                    explorer_url = f"https://solscan.io/tx/{txid}"
                                    st.markdown(f"View transaction on Solana Explorer: [TX {txid[:10]}...]({explorer_url})")
                            st.json(result)
                        else:
                            st.error(f"Error: {response.json().get('detail')}")
                except Exception as e:
                    st.error(f"Failed to sign transaction: {str(e)}")
    # Navigation buttons
    render_navigation_buttons()

elif current_page == "Authorize Queued Tx":
    st.markdown('<h1 class="main-header">Authorize Queued Transaction</h1>', unsafe_allow_html=True)
    with st.container():
        with st.form("authorize_form"):
            st.markdown('<div class="subsection-header">Authorization Details</div>', unsafe_allow_html=True)
        
            txn_id = st.text_input("Transaction ID", placeholder="Enter the queued transaction ID")
            shards_input = st.text_area("Enhanced Shards (one per line)",
                                      placeholder="Provide additional security shards as required",
                                      height=150)
            level = st.selectbox("Required Level", ["tier1", "tier2", "tier3"],
                                 help="Required security level (tier1 = highest priority)")
        
            submitted = st.form_submit_button("Authorize Transaction", use_container_width=True)
        
            if submitted:
                shards = [s.strip() for s in shards_input.split("\n") if s.strip()]
                data = {
                    "txn_id": txn_id,
                    "shards": shards,
                    "level": level
                }
                try:
                    with st.spinner("Processing enhanced security authorization..."):
                        response = requests.post(f"{API_BASE}/transactions/authorize_queued_tx", json=data)
                        if response.status_code == 200:
                            st.success("✅ Transaction authorized and broadcasted successfully!")
                            result = response.json()
                            txid = result.get('txid')
                            if txid:
                                explorer_url = f"https://solscan.io/tx/{txid}"
                                st.markdown(f"View transaction on Solana Explorer: [TX {txid[:10]}...]({explorer_url})")
                            st.json(result)
                        else:
                            st.error(f"Error: {response.json().get('detail')}")
                except Exception as e:
                    st.error(f"Failed to authorize: {str(e)}")
    # Navigation buttons
    render_navigation_buttons()

elif current_page == "Pending Transactions":
    st.markdown('<h1 class="main-header">Pending Transactions</h1>', unsafe_allow_html=True)
    try:
        with st.spinner("Loading pending transactions..."):
            response = requests.get(f"{API_BASE}/transactions/pending")
            if response.status_code == 200:
                data = response.json()
                if data["count"] > 0:
                    st.markdown(f'<div class="subsection-header">{data["count"]} Pending Transactions</div>', unsafe_allow_html=True)
                   
                    for txn in data["pending_transactions"]:
                        with st.expander(f"TX: {txn.get('txn_id', 'Unknown')} - ${txn.get('amount', 0)}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Wallet:** {txn.get('wallet_id')}")
                                st.write(f"**To:** {txn.get('to_address')[:20]}...")
                                st.write(f"**Amount:** ${txn.get('amount')} {txn.get('token_symbol', 'SOL')}")
                            with col2:
                                st.write(f"**Level:** {txn.get('escalation_level', 'tier1')}")
                                if txn.get('flagged'):
                                    st.warning("**Flagged:** Potential fraud detected")
                
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Refresh List", use_container_width=True):
                            st.rerun()
                    with col2:
                        if st.button("Authorize Transaction", use_container_width=True):
                            st.session_state.current_page = "Authorize Queued Tx"
                            st.rerun()
                else:
                    st.info("No pending transactions requiring authorization")
            else:
                st.error("Failed to fetch pending transactions")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    # Navigation buttons
    render_navigation_buttons()

elif current_page == "Wallets":
    st.markdown('<h1 class="main-header">Wallet Management</h1>', unsafe_allow_html=True)
    try:
        with st.spinner("Loading wallet information..."):
            response = requests.get(f"{API_BASE}/wallets")
            if response.status_code == 200:
                data = response.json()
                if data["count"] > 0:
                    st.markdown(f'<div class="subsection-header">{data["count"]} Active Wallets</div>', unsafe_allow_html=True)
                
                    for wallet in data["wallets"]:
                        with st.expander(f"{wallet.get('wallet_id', 'Unknown')} - {wallet.get('pubkey', '')[:20]}..."):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Scheme:** {wallet.get('scheme', 'N/A')}")
                                st.write(f"**Public Key:** {wallet.get('pubkey', 'N/A')}")
                            with col2:
                                st.write(f"**Shards:** {len(wallet.get('shards', []))}")
                                st.write(f"**Created:** {wallet.get('created_at', 'N/A')}")
                
                    st.table(data["wallets"])
                else:
                    st.info("No wallets created yet. Create your first wallet to get started!")
            else:
                st.error("Failed to fetch wallets")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    # Navigation buttons
    render_navigation_buttons()

# Professional footer
st.markdown("""
<div class="footer">
    StableFlow Pay MVP
</div>
""", unsafe_allow_html=True)
