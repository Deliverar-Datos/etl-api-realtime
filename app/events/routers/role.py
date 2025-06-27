from fastapi import APIRouter, HTTPException, Request, logger
from ldap3 import Server, Connection, NTLM, ALL, SUBTREE


router = APIRouter()

@router.get("/role")
async def get_role(
    request: Request
):
    try:
        email = request.query_params.get("email")

        role = get_user_groups_by_upn(email)

        return {
            "role": role
        }
       
    except Exception as e:
        logger.error(f"error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



def get_user_groups_by_upn(upn):
    # Define LDAP connection
    server = Server('ad.deliver.ar', port=389, use_ssl=False, get_info=ALL)

    conn = Connection(
        server,
        user='DELIVERAR\\svc-bi',
        password='Welcome2025!',
        authentication=NTLM,
        auto_bind=False
    )

    if conn.start_tls():
        if conn.bind():
#            print("✅ Authentication succeeded (via StartTLS)")

            base_dn = 'DC=deliver,DC=ar'
            search_filter = f'(&(objectClass=user)(userPrincipalName={upn}))'
            attributes = ['memberOf', 'distinguishedName', 'userPrincipalName']

            conn.search(
                search_base=base_dn,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=attributes
            )

            if conn.entries:
                user_entry = conn.entries[0]
                for group in user_entry.memberOf:
                    # Extract only the CN part from the LDAP DN
                    if group.startswith('CN='):
                        cn_part = group.split(',')[0]  # Get the first part (CN=...)
                        cn_value = cn_part.replace('CN=', '')  # Remove the CN= prefix
                        return cn_value
                    return group  # Fallback to return the full DN if it doesn't start with CN=
            else:
                raise Exception(f"❌ User with UPN '{upn}' not found.")
        else:
            raise Exception("❌ Bind failed:", conn.result)
    else:
        raise Exception("❌ StartTLS failed:", conn.result)
