import random
from collections import defaultdict
import pandas as pd


class UnionFind:
    """Simple Union-Find implementation"""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1


class SocialNetwork:
    def __init__(self, custom_user=None):
        self.users = {}
        self.graph = defaultdict(set)              # Graph (Adjacency List)
        self.friend_requests = defaultdict(set)   # Incoming requests
        self.sent_requests = defaultdict(dict)    # Sent requests with status

        # Add custom user first if provided
        if custom_user:
            self.users[custom_user["name"]] = {
                "age": custom_user.get("age", 25),
                "city": custom_user.get("city", "Mumbai"),
                "interest": custom_user.get("interest", "Gaming"),
                "profession": custom_user.get("profession", "Engineer"),
                "skills": custom_user.get("skills", ["Python", "Data Analysis"]),
                "company": custom_user.get("company", "Startup"),
                "education": custom_user.get("education", "B.Tech"),
                "hobby": custom_user.get("hobby", "Cricket"),
                "language": custom_user.get("language", "English")
            }
        
        self._load_users_from_csv()

    # -------------------------------------------------
    # Load Users from CSV
    # -------------------------------------------------
    def _load_users_from_csv(self):
        try:
            df = pd.read_csv("social_dataset.csv")
            for _, row in df.iterrows():
                name = row["Name"]
                if name not in self.users:  # Skip if custom user already added
                    self.users[name] = {
                        "age": random.randint(18, 40),  # Random age since not in CSV
                        "city": row["City"],
                        "interest": row["Interest"],
                        "profession": row["Profession"],
                        "skills": [row["Skill"]],  # Single skill as list
                        "company": row["Company"],
                        "education": row["Education"],
                        "hobby": row["Hobby"],
                        "language": row["Language"]
                    }
        except FileNotFoundError:
            print("Warning: social_dataset.csv not found. No users loaded.")

    # -------------------------------------------------
    # Recommendation Logic
    # -------------------------------------------------
    def recommend(self, user):
        """Return up to 10 random friend suggestions.

        Preferences:
        1. Fill with friends-of-friends if available.
        2. Otherwise pick random non-friends.
        """
        # gather second-degree connections
        fof = set()
        for friend in self.graph[user]:
            fof.update(self.graph[friend])
        # remove user and direct friends
        fof.discard(user)
        fof -= self.graph[user]

        max_suggestions = 10
        chosen = []
        if fof:
            sample_size = min(len(fof), max_suggestions)
            chosen = random.sample(fof, sample_size)
        if len(chosen) < max_suggestions:
            # fill with other random candidates
            candidates = [o for o in self.users if o != user and o not in self.graph[user] and o not in chosen]
            need = max_suggestions - len(chosen)
            if candidates:
                chosen += random.sample(candidates, min(need, len(candidates)))
        # return list of tuples with dummy score
        return [(u, 0) for u in chosen]

    # -------------------------------------------------
    # Send Multiple Friend Requests with Random Response
    # -------------------------------------------------
    def send_friend_requests_batch(self, sender, receivers, randomize: bool = False):
        """Send requests to multiple users.

        By default the outgoing requests are marked **Pending** and the receiver
        must later accept or reject them.  If ``randomize`` is ``True`` the
        behaviour mirrors the original prototype: each request is immediately
        resolved with a random decision (0=accept,1=reject,2=pending) to simulate
        a quick automated response from the other user.

        Returns a dictionary with keys ``total_sent``, ``accepted``, ``rejected``
        and ``pending`` listing the affected receivers.
        """
        sent_requests = []
        accepted = []
        rejected = []
        pending = []

        for receiver in receivers:
            # skip if already friends or already sent
            if receiver not in self.graph[sender] and receiver not in self.sent_requests[sender]:
                self.friend_requests[receiver].add(sender)
                sent_requests.append(receiver)

                if randomize:
                    decision = random.randint(0, 2)
                    if decision == 0:
                        # accept immediately
                        self.graph[sender].add(receiver)
                        self.graph[receiver].add(sender)
                        self.sent_requests[sender][receiver] = "Accepted"
                        accepted.append(receiver)
                        if sender in self.friend_requests[receiver]:
                            self.friend_requests[receiver].remove(sender)
                    elif decision == 1:
                        self.sent_requests[sender][receiver] = "Rejected"
                        rejected.append(receiver)
                        if sender in self.friend_requests[receiver]:
                            self.friend_requests[receiver].remove(sender)
                    else:
                        self.sent_requests[sender][receiver] = "Pending"
                        pending.append(receiver)
                else:
                    # simply mark pending
                    self.sent_requests[sender][receiver] = "Pending"
                    pending.append(receiver)

        return {
            "total_sent": len(sent_requests),
            "accepted": accepted,
            "rejected": rejected,
            "pending": pending
        }

    # -------------------------------------------------
    # Auto Accept 20% of Sent Requests (unchanged)
    # -------------------------------------------------
    def auto_accept_20_percent(self, user):
        # Only get pending requests
        pending = [u for u, status in self.sent_requests[user].items() if status == "Pending"]

        if not pending:
            return []

        accept_count = max(1, int(0.2 * len(pending)))
        accepted = random.sample(pending, min(accept_count, len(pending)))

        for receiver in accepted:
            # Add friendship (Graph update)
            self.graph[user].add(receiver)
            self.graph[receiver].add(user)

            # Update status
            self.sent_requests[user][receiver] = "Accepted"

            # Remove from pending list
            if user in self.friend_requests[receiver]:
                self.friend_requests[receiver].remove(user)

        return accepted

    # -------------------------------------------------
    # Reject Friend Request(s) (as sender)
    # -------------------------------------------------
    def reject_requests(self, user, requests_to_reject):
        rejected = []

        for receiver in requests_to_reject:
            if receiver in self.sent_requests[user]:
                self.sent_requests[user][receiver] = "Rejected"

                if user in self.friend_requests[receiver]:
                    self.friend_requests[receiver].remove(user)

                rejected.append(receiver)

        return rejected

    # -------------------------------------------------
    # Get Sent Requests Table
    # -------------------------------------------------
    def get_sent_requests_table(self, user):
        data = []

        for receiver, status in self.sent_requests[user].items():
            data.append({
                "To User": receiver,
                "Status": status
            })

        return pd.DataFrame(data)

    # -------------------------------------------------
    # Incoming requests for a user
    # -------------------------------------------------
    def get_incoming_requests(self, user):
        """Return a list of users who have sent a request to **user**."""
        return list(self.friend_requests[user])

    # -------------------------------------------------
    # Received requests status table
    # -------------------------------------------------
    def get_received_requests_table(self, user):
        """Return a DataFrame summarizing the status of requests that *others* have
        sent to **user**.  This inspects the sent_requests dictionary of every
        other user.
        """
        data = []
        for sender, sent in self.sent_requests.items():
            if user in sent:
                data.append({
                    "From User": sender,
                    "Status": sent[user]
                })
        return pd.DataFrame(data)

    def generate_random_incoming(self, user, n=5):
        """Create **n** random pending requests targeting *user*.

        Useful for simulating a busy network in which others send you requests.
        Already-existing incoming requests are left alone; new ones are always
        marked pending on both sides.
        """
        candidates = [u for u in self.users if u != user and u not in self.graph[user] and u not in self.friend_requests[user]]
        random.shuffle(candidates)
        created = []
        for sender in candidates[:n]:
            self.friend_requests[user].add(sender)
            self.sent_requests[sender][user] = "Pending"
            created.append(sender)
        return created

    def randomly_process_incoming(self, user):
        """Process **user**'s incoming requests with random outcomes.

        Each sender still has a chance to be accepted, rejected or remain pending.
        The caller does not control the result; it is returned for display.
        """
        accepted = []
        rejected = []
        pending = []

        for sender in list(self.friend_requests[user]):
            decision = random.randint(0, 2)
            if decision == 0:
                # accept
                self.graph[user].add(sender)
                self.graph[sender].add(user)
                self.sent_requests[sender][user] = "Accepted"
                accepted.append(sender)
                self.friend_requests[user].remove(sender)
            elif decision == 1:
                self.sent_requests[sender][user] = "Rejected"
                rejected.append(sender)
                self.friend_requests[user].remove(sender)
            else:
                # remain pending (leave in friend_requests)
                pending.append(sender)
        return {"accepted": accepted, "rejected": rejected, "pending": pending}

    # -------------------------------------------------
    # Randomly process pending sent requests for a user
    # -------------------------------------------------
    def randomly_process_sent_requests(self, sender, rounds: int = 1):
        """Randomly resolve pending outgoing requests created by *sender*.

        For every receiver with a "Pending" status in ``self.sent_requests[sender]``
        this will randomly choose to Accept, Reject, or leave Pending. If
        ``rounds`` &gt; 1 then pending entries get additional chances to resolve.

        Returns a dict summarizing accepted/rejected/pending lists (only for the
        items that were pending at the start of this call).
        """
        # collect initial pending set so we return results only for these
        initial_pending = [r for r, s in self.sent_requests[sender].items() if s == "Pending"]

        for _ in range(max(1, rounds)):
            # iterate snapshot to avoid mutation issues
            for receiver, status in list(self.sent_requests[sender].items()):
                if status != "Pending":
                    continue
                decision = random.randint(0, 2)
                if decision == 0:
                    # accept
                    self.graph[sender].add(receiver)
                    self.graph[receiver].add(sender)
                    self.sent_requests[sender][receiver] = "Accepted"
                    if sender in self.friend_requests[receiver]:
                        self.friend_requests[receiver].remove(sender)
                elif decision == 1:
                    # reject
                    self.sent_requests[sender][receiver] = "Rejected"
                    if sender in self.friend_requests[receiver]:
                        self.friend_requests[receiver].remove(sender)
                else:
                    # remain pending; may be retried in the next round
                    pass

        # build result lists constrained to initial pending set
        accepted = [r for r in initial_pending if self.sent_requests[sender].get(r) == "Accepted"]
        rejected = [r for r in initial_pending if self.sent_requests[sender].get(r) == "Rejected"]
        pending = [r for r in initial_pending if self.sent_requests[sender].get(r) == "Pending"]

        return {"accepted": accepted, "rejected": rejected, "pending": pending}

    # -------------------------------------------------
    # Respond to incoming requests
    # -------------------------------------------------
    def respond_to_requests(self, user, accepts=None, rejects=None):
        """Allow **user** to accept or reject incoming requests.

        ``accepts`` and ``rejects`` are iterables of usernames.  Only those
        present in the ``friend_requests`` set for ``user`` are processed.
        Returns a dict summarizing what was done.
        """
        accepts = accepts or []
        rejects = rejects or []
        accepted = []
        rejected = []

        for sender in accepts:
            if sender in self.friend_requests[user]:
                # create bidirectional friendship
                self.graph[user].add(sender)
                self.graph[sender].add(user)
                self.sent_requests[sender][user] = "Accepted"
                self.friend_requests[user].remove(sender)
                accepted.append(sender)

        for sender in rejects:
            if sender in self.friend_requests[user]:
                self.sent_requests[sender][user] = "Rejected"
                self.friend_requests[user].remove(sender)
                rejected.append(sender)

        return {"accepted": accepted, "rejected": rejected}

    # -------------------------------------------------
    # Union-Find: get communities of size >= 2
    # -------------------------------------------------
    def get_friend_communities(self):
        username_to_id = {user: idx for idx, user in enumerate(self.users.keys())}
        uf = UnionFind(len(self.users))
        for user, friends in self.graph.items():
            uid = username_to_id[user]
            for f in friends:
                fid = username_to_id[f]
                uf.union(uid, fid)
        communities = defaultdict(list)
        for user, uid in username_to_id.items():
            root = uf.find(uid)
            communities[root].append(user)
        # filter size>=2
        return [c for c in communities.values() if len(c) >= 2]