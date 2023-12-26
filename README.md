# hospi

## 2023-12 updates

### hn_sale module

Edit sequences:
1. CO Sale Sequence, rename to OEM Sale Sequence, change padding to 4, change prefix to OEM
2. Sale Order Sequence, rename to Reguler Sale Sequence, change padding to 4

Need to update old records to this specification:
1. those with co_sale TRUE should have oem as their order type.
2. those with co_sale FALSE should have reguler as their order type.
It's recommended to use mass export+import to perform this update.

### purchase_request module

We introduce another approver (level-2 approver) to the standard purchase request module. The user can be assigned to a request by filling in Approver 2 field on creation or before request approval phase. FYI we relabel the original Approver to Approver 1.

<span style="color:#FF0000">We assume that level-2 approvers are just approvers; they do not create RFQ or "done" a request, etc. They can still reject it though.</span>

We also introduce Approve 2 state in addition to Approved (which now is relabeled to Approve 1). Requests that have no level-2 approvers will go straight to Approve 2 from To Approve state. Clicking Done while on Approve 1 will result in error if Approver 2 was filled in. In other words, Approve 2 is the new Approve state while Approve 1 is just an intermediary one.

We keep Purchase Request Manager as level-1 approver, and imply Purchase Request User group. We add a new group, Purchase Request Level-2 Approver. Please note that this group does not imply Purchase Request User, since it is assumed the user can be from another division, director, or even owner. Set a user to both Purchase Request Manager and Purchase Request Level-2 Approver if you'd like them to have purchase-manager-level access too.

**Action Items**

Need to add users to Purchase Request Level-2 Approver group.

Requests that's currently on Approve 1 ("approved" in database) state should be changed to Approve 2 ("approved2" in database). Since they are assumed to not have Approver 2, performing this to all Approve 1 ones should be safe. Mass export+import is recommended.

The purchase request module's creators calls for empty record rule so admins can adjust them according to needs. We just follow this convention when adding new ones, but here's what I did regarding rule on staging:
- Purchase Request Line Level-2 Approver: Rule Definition is [('assigned_to2','=',user.id)]
- Purchase Request Level-2 Approver: Rule Definition is the same
This means that level-2 approvers can only see his/her assigned requests. After approving a request it is automatically gone from the user's list. Feel free to set these on live.

### Document Number

We now have Document Number field under every report on Settings | Technical | Reporting | Reports. First of all fill the field in for the appropriate reports, preferably those which are printed as form (like invoice, purchase request, etc). This field is then available in all report xml as document_no variable.

As an example, let's edit report's footer and print document_no if one exists for the form:

```html
    <div t-attf-class="footer o_clean_footer o_company_#{company.id}_layout">
      ...
      <span t-if="document_no">Form No: <t t-esc="document_no" /></span>
    </div>

(the code above can be edited in via Settings | General Settings | (Business Documents section) | Edit Layout button)

Special note: as per late December 2023, purchase requests need below action to be able to be printed:

Go to Settings | Technical | Reports | (click Purchase Request)

Then click "Add in the 'Print' menu" button. Please be aware that this will show the print button for all users.