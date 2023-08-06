
Let's create repository using default parameters:

  $ hg bb_create utst_first
  Creating BitBucket repo Mekk/utst_first
  Repository created
  
  Repository: Mekk/utst_first  (scm: hg, size: *.* kB) (glob)
  Access: private   (owner: Mekk)
  Issues: no, wiki: no, forks: private, language: 
  Paths:
      (https)    https://Mekk@bitbucket.org/Mekk/utst_first
      (ssh)      ssh://hg@bitbucket.org/Mekk/utst_first
  No description
  
  Now `hg push https://bitbucket.org/Mekk/utst_first` to push the code
  Visit https://bitbucket.org/Mekk/utst_first to review details

Reviewing status:

  $ hg bb_status utst_first
  Checking status of BitBucket repo utst_first belonging to Mekk
  
  Repository: Mekk/utst_first  (scm: hg, size: *.* kB) (glob)
  Access: private   (owner: Mekk)
  Issues: no, wiki: no, forks: private, language: 
  Paths:
      (https)    https://Mekk@bitbucket.org/Mekk/utst_first
      (ssh)      ssh://hg@bitbucket.org/Mekk/utst_first
  No description

Trying to modify:

  $ hg bb_modify utst_first --public --issues --descr='Updated descr'
  Applying BitBucket metadata changes (API v1)
  Changes saved
  
  Repository: Mekk/utst_first  (scm: hg, size: *.* kB) (glob)
  Access: public   (owner: Mekk)
  Issues: yes, wiki: no, forks: public, language: 
  Paths:
      (https)    https://Mekk@bitbucket.org/Mekk/utst_first
      (ssh)      ssh://hg@bitbucket.org/Mekk/utst_first
  Description:
      Updated descr

Modify with bad options:

  $ hg bb_modify utst_first --forks=no --public
  Applying BitBucket metadata changes (API v1)
  
  Failed to modify BitBucket repository: Public repositories must allow forks.
  [1]

Cleaning up:

  $ hg bb_delete --force utst_first
  
  Repository: Mekk/utst_first  (scm: hg, size: *.* kB) (glob)
  Access: public   (owner: Mekk)
  Issues: yes, wiki: no, forks: public, language: 
  Paths:
      (https)    https://Mekk@bitbucket.org/Mekk/utst_first
      (ssh)      ssh://hg@bitbucket.org/Mekk/utst_first
  Description:
      Updated descr
  Deleting BitBucket clone Mekk/utst_first
  BitBucket clone deleted

Verifying whether it is missing:

  $ hg bb_status utst_first
  Checking status of BitBucket repo utst_first belonging to Mekk
  
  Repository Mekk/utst_first does not exist on BitBucket
  [1]
