import streamlit as st
from social_network import SocialNetwork

# Initialize with sidebar setup
if "sn" not in st.session_state:
    st.session_state.sn = None
    st.session_state.current_user = None

# Sidebar - Profile Setup
with st.sidebar:
    st.title("⚙️ Setup Your Profile")
    
    with st.form("profile_form"):
        name = st.text_input("Your Name *", placeholder="e.g., John Doe")
        age = st.slider("Age", 18, 50, 25)
        city = st.selectbox("City", ["Mumbai", "Delhi", "Bangalore", "Pune", "Chennai", "Hyderabad"])
        
        interests = st.multiselect(
            "Your Interests *",
            ["AI", "ML", "Finance", "Gaming", "Sports", "Music", "Coding", "Blockchain"],
            default=["Gaming"]
        )
        
        profession = st.selectbox("Profession", ["Student", "Engineer", "Doctor", "Designer", "Trader", "Entrepreneur"])
        
        skills = st.multiselect(
            "Skills",
            ["Python", "Java", "C++", "Data Analysis", "Machine Learning", "UI/UX", "Marketing", "Stock Trading", "Cloud"],
            default=["Python", "Data Analysis"]
        )
        
        company = st.selectbox("Company", ["TCS", "Infosys", "Google", "Microsoft", "Amazon", "Flipkart", "Startup"])
        education = st.selectbox("Education", ["B.Tech", "MBA", "B.Sc", "M.Tech", "B.Com", "PhD"])
        hobby = st.selectbox("Hobby", ["Cricket", "Football", "Reading", "Traveling", "Photography", "Chess"])
        language = st.selectbox("Language", ["English", "Hindi", "Marathi", "Tamil", "Telugu", "Kannada"])
        
        submitted = st.form_submit_button("Create Profile", use_container_width=True)
        
        if submitted:
            if name and interests:
                custom_user = {
                    "name": name,
                    "age": age,
                    "city": city,
                    "interest": interests[0],  # Primary interest
                    "profession": profession,
                    "skills": skills,
                    "company": company,
                    "education": education,
                    "hobby": hobby,
                    "language": language
                }
                st.session_state.sn = SocialNetwork(custom_user=custom_user)
                st.session_state.current_user = name
                st.success(f"✅ Profile created! Welcome, {name}!")
                st.rerun()
            else:
                st.error("Please fill in Name and select at least one Interest")

# Main content - only show if user is created
if st.session_state.sn is None:
    st.title("🔥 Social Network Friend Recommendation Engine")
    st.info("👈 Create your profile in the sidebar to get started!")
else:
    sn = st.session_state.sn
    current_user = st.session_state.current_user

    st.title("🔥 Social Network Friend Recommendation Engine")
    
    # Show current user
    user_info = sn.users[current_user]
    st.markdown(f"### 👤 Logged in as: **{current_user}** | {user_info['city']} | {user_info['profession']}")

    st.divider()

    # ----------------------------------------
    # Friend Recommendations
    # ----------------------------------------
    st.subheader("🤝 Recommended Friends")

    # allow user to refresh list whenever they want
    if st.button("Refresh Recommendations"):
        st.session_state.recs = sn.recommend(current_user)
        st.session_state.just_sent = True  # clear previous checkbox state
        # generate a few random incoming requests each time we refresh
        sn.generate_random_incoming(current_user, n=5)

    # make recommendations always visible by default
    if "recs" not in st.session_state:
        st.session_state.recs = sn.recommend(current_user)
        # also seed some random incoming requests on first load
        sn.generate_random_incoming(current_user, n=5)

    # (auto-response removed) outgoing requests are always pending by default

    # ensure the flag is always true so we render the block
    if True:
        # if we just sent requests, clear any previous checkbox state before rendering
        if st.session_state.get("just_sent", False):
            for user, _ in st.session_state.get("recs", []):
                key = f"rec_{user}"
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.just_sent = False

        # use stored recommendations (fallback to generate if missing)
        recs = st.session_state.get("recs", [])
        if not recs:
            recs = sn.recommend(current_user)
            st.session_state.recs = recs

        if recs:
            st.write("**Select users to send requests:**")

            for user, score in recs:
                st.checkbox(
                    f"{user} (Score: {score})",
                    key=f"rec_{user}",
                    value=st.session_state.get(f"rec_{user}", False)
                )

            selected_users = [user for user, score in recs if st.session_state.get(f"rec_{user}", False)]

            if selected_users:
                if st.button(f"Send Requests to {len(selected_users)} User(s)"):
                    # always send as pending (no auto-response)
                    result = sn.send_friend_requests_batch(current_user, selected_users, randomize=False)

                    st.success(f"📤 Sent {result['total_sent']} request(s). They are now pending.")

                    # automatically process sent requests with random outcomes
                    auto_res = sn.randomly_process_sent_requests(current_user, rounds=3)
                    parts = []
                    if auto_res.get("accepted"):
                        parts.append(f"✅ {len(auto_res['accepted'])} accepted")
                    if auto_res.get("rejected"):
                        parts.append(f"❌ {len(auto_res['rejected'])} rejected")
                    if auto_res.get("pending"):
                        parts.append(f"⏳ {len(auto_res['pending'])} still pending")
                    if parts:
                        st.info("Auto-processed sent requests: " + "; ".join(parts))

                    # mark that we've sent so the next run resets boxes
                    st.session_state.just_sent = True

                    # refresh the table immediately
                    st.rerun()
        else:
            st.write("No recommendations available.")

    st.divider()

    # ----------------------------------------
    # Incoming Friend Requests (as recipient)
    # ----------------------------------------
    st.subheader("📥 Incoming Requests")
    incoming = sn.get_incoming_requests(current_user)
    if incoming:
        st.write(f"You have {len(incoming)} incoming request(s). Please choose Accept or Reject for each, then press Process Incoming.")
        # render a radio for each incoming sender so the user can decide
        for sender in incoming:
            # default to Pending
            st.radio(f"From {sender}", ["Pending", "Accept", "Reject"], key=f"dec_{sender}", index=0)

        if st.button("Process Incoming"):
            accepts = [s for s in incoming if st.session_state.get(f"dec_{s}") == "Accept"]
            rejects = [s for s in incoming if st.session_state.get(f"dec_{s}") == "Reject"]
            res = sn.respond_to_requests(current_user, accepts=accepts, rejects=rejects)
            msg = []
            if res.get("accepted"):
                msg.append(f"✅ Accepted: {', '.join(res['accepted'])}")
            if res.get("rejected"):
                msg.append(f"❌ Rejected: {', '.join(res['rejected'])}")
            st.info("; ".join(msg))
            # clear per-sender decision keys
            for sender in incoming:
                key = f"dec_{sender}"
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    else:
        st.write("No incoming requests.")

    st.divider()

    # ----------------------------------------
    # Friend Requests Status
    # ----------------------------------------
    st.subheader("📊 Request Status")

    sent_df = sn.get_sent_requests_table(current_user)
    # some older sn instances may not have the helper method (due to cached session)
    if hasattr(sn, "get_received_requests_table"):
        recv_df = sn.get_received_requests_table(current_user)
    else:
        # build table manually
        import pandas as _pd
        rows = []
        for sender, sent in sn.sent_requests.items():
            if current_user in sent:
                rows.append({"From User": sender, "Status": sent[current_user]})
        recv_df = _pd.DataFrame(rows)

    # display both tables side by side
    if not sent_df.empty or not recv_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📤 Sent Requests")
            if not sent_df.empty:
                st.dataframe(sent_df)
                accepted_count = len(sent_df[sent_df["Status"] == "Accepted"])
                pending_count = len(sent_df[sent_df["Status"] == "Pending"])
                rejected_count = len(sent_df[sent_df["Status"] == "Rejected"])
                st.metric("Accepted", accepted_count)
                st.metric("Pending", pending_count)
                st.metric("Rejected", rejected_count)
            else:
                st.write("None")
        with col2:
            st.subheader("📥 Received Requests")
            if not recv_df.empty:
                st.dataframe(recv_df)
                acc2 = len(recv_df[recv_df["Status"] == "Accepted"])
                pen2 = len(recv_df[recv_df["Status"] == "Pending"])
                rej2 = len(recv_df[recv_df["Status"] == "Rejected"])
                st.metric("Accepted", acc2)
                st.metric("Pending", pen2)
                st.metric("Rejected", rej2)
            else:
                st.write("None")

        # combined table for convenience
        import pandas as _pd
        combined = None
        if not sent_df.empty:
            temp = sent_df.copy()
            temp["Direction"] = "Sent"
            combined = temp
        if not recv_df.empty:
            temp2 = recv_df.copy()
            temp2 = temp2.rename(columns={"From User": "User"})
            temp2["Direction"] = "Received"
            temp2 = temp2[["User", "Status", "Direction"]]
            if combined is None:
                combined = temp2
            else:
                # sent table uses "To User" column; rename for consistency
                combined = combined.rename(columns={"To User": "User"})
                combined = _pd.concat([combined, temp2], ignore_index=True)
        if combined is not None:
            st.subheader("🔁 All Requests")
            st.dataframe(combined)
    else:
        st.write("No requests have been exchanged yet.")

    # sent requests are auto-processed immediately after sending

    st.divider()

    # ----------------------------------------
    # Friend Communities
    # ----------------------------------------
    st.subheader("👥 Friend Communities")
    communities = sn.get_friend_communities()
    if communities:
        for i, comm in enumerate(communities, 1):
            with st.expander(f"Community {i} ({len(comm)} members)"):
                st.write(", ".join(sorted(comm)))
    else:
        st.info("No communities with 2 or more people found.")